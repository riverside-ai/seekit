from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
import json
from json import JSONDecoder
import re
from typing import Any
from urllib.parse import quote, quote_plus, urljoin, urlsplit, urlunsplit

import curl_cffi
import lxml.html
from pydantic import BaseModel


@dataclass(frozen=True)
class RequestTemplate:
    method: str
    url: str
    headers: dict[str, str]
    cookies: dict[str, str]
    body: str | None = None


class SerpItem(BaseModel):
    provider: str
    title: str | None = None
    excerpt: str | None = None
    url: str | None = None
    author: str | None = None
    cover_url: str | None = None
    time: str | None = None


KEYWORD_PLACEHOLDER = "OpenClaw"


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", value).strip()
    return text or None


def strip_html(value: str | None) -> str | None:
    if not value:
        return None
    fragment = lxml.html.fromstring(f"<div>{value}</div>")
    return clean_text(fragment.text_content())


def take_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, dict):
        if "simpleText" in value:
            return clean_text(value["simpleText"])
        if "text" in value and isinstance(value["text"], str):
            return clean_text(value["text"])
        if "runs" in value:
            return clean_text("".join(run.get("text", "") for run in value["runs"]))
        if "fragments" in value:
            return clean_text(
                "".join(fragment.get("plaintext", "") for fragment in value["fragments"])
            )
    if isinstance(value, list):
        return clean_text(" ".join(part for part in (take_text(item) for item in value) if part))
    return None


def absolutize_url(value: str | None, base_url: str | None = None) -> str | None:
    value = clean_text(value)
    if not value:
        return None
    if value.startswith("//"):
        return "https:" + value
    if base_url:
        return urljoin(base_url, value)
    return value


@cache
def extract_json_from_text(text: str) -> Any:
    candidates = [index for index in (text.find("{"), text.find("[")) if index != -1]
    if not candidates:
        raise ValueError("No JSON payload found in response body.")
    start = min(candidates)
    payload, _ = JSONDecoder().raw_decode(text[start:])
    return payload


def replace_placeholder(value: str, placeholder: str = KEYWORD_PLACEHOLDER) -> str:
    replacements = (
        (quote_plus(placeholder), "{keyword_plus}"),
        (quote(placeholder, safe=""), "{keyword_quoted_strict}"),
        (quote(placeholder), "{keyword_quoted}"),
        (placeholder, "{keyword}"),
    )
    result = value
    for source, template in replacements:
        result = result.replace(source, template)
    return result


def url_to_template(url: str) -> str:
    parts = urlsplit(url)
    path = replace_placeholder(parts.path)
    query_parts: list[str] = []
    if parts.query:
        for chunk in parts.query.split("&"):
            if "=" in chunk:
                key, value = chunk.split("=", 1)
                query_parts.append(f"{replace_placeholder(key)}={replace_placeholder(value)}")
            else:
                query_parts.append(replace_placeholder(chunk))
    query = "&".join(query_parts)
    fragment = replace_placeholder(parts.fragment)
    return urlunsplit((parts.scheme, parts.netloc, path, query, fragment))


def render_template(value: str, keyword: str) -> str:
    return value.format(
        keyword=keyword,
        keyword_plus=quote_plus(keyword),
        keyword_quoted=quote(keyword),
        keyword_quoted_strict=quote(keyword, safe=""),
    )


def build_request_template(
    *,
    method: str,
    url: str,
    headers: dict[str, str],
    cookies: dict[str, str],
    body: str | None = None,
) -> RequestTemplate:
    return RequestTemplate(
        method=method,
        url=url_to_template(url),
        headers={name: replace_placeholder(value) for name, value in headers.items()},
        cookies={name: replace_placeholder(value) for name, value in cookies.items()},
        body=replace_placeholder(body) if body is not None else None,
    )


class BaseSERP(ABC):
    provider: str = ""
    base_url: str | None = None
    request_template: RequestTemplate | None = None

    def pick_entry(self, entries: list[dict[str, Any]]) -> dict[str, Any]:
        return entries[0]

    def get_request_template(self, keyword: str) -> RequestTemplate:
        if self.request_template is None:
            raise ValueError(f"{self.provider} does not define a request template.")
        template = self.request_template
        return RequestTemplate(
            method=template.method,
            url=render_template(template.url, keyword),
            headers={name: render_template(value, keyword) for name, value in template.headers.items()},
            cookies={name: render_template(value, keyword) for name, value in template.cookies.items()},
            body=render_template(template.body, keyword) if template.body is not None else None,
        )

    def request(self, keyword: str) -> str:
        template = self.get_request_template(keyword)
        headers = {
            name: value
            for name, value in template.headers.items()
            if name.lower() != "content-length"
        }
        response = curl_cffi.request(
            method=template.method,
            url=template.url,
            headers=headers,
            cookies=template.cookies,
            data=template.body,
            impersonate="chrome",
        )
        return response.text

    @abstractmethod
    def parse_response(self, body: str) -> list[SerpItem]:
        raise NotImplementedError

    def query(self, keyword: str) -> list[SerpItem]:
        return self.parse_response(self.request(keyword))

    def make_item(
        self,
        *,
        title: str | None,
        excerpt: str | None,
        url: str | None,
        author: str | None = None,
        cover_url: str | None = None,
        time: str | None = None,
        base_url: str | None = None,
    ) -> SerpItem | None:
        title = clean_text(title)
        excerpt = clean_text(excerpt)
        author = clean_text(author)
        time = clean_text(time)
        url = absolutize_url(url, base_url or self.base_url)
        cover_url = absolutize_url(cover_url, base_url or self.base_url)
        if not any([title, excerpt, url]):
            return None
        return SerpItem(
            provider=self.provider,
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
            cover_url=cover_url,
            time=time,
        )


class HtmlSERP(BaseSERP):
    item_xpath: str = ""

    def parse_response(self, body: str) -> list[SerpItem]:
        tree = lxml.html.fromstring(body)
        items: list[SerpItem] = []
        for node in tree.xpath(self.item_xpath):
            item = self.parse_node(node)
            if item is not None:
                items.append(item)
        return items

    @abstractmethod
    def parse_node(self, node: Any) -> SerpItem | None:
        raise NotImplementedError

    def first_text(self, node: Any, *xpaths: str) -> str | None:
        for xpath in xpaths:
            values = node.xpath(xpath)
            if not values:
                continue
            first = values[0]
            if isinstance(first, str):
                text = clean_text(first)
            else:
                text = clean_text(first.text_content())
            if text:
                return text
        return None

    def first_attr(self, node: Any, xpath: str) -> str | None:
        values = node.xpath(xpath)
        if not values:
            return None
        return clean_text(values[0])

    def fallback_excerpt(self, node: Any, title: str | None) -> str | None:
        text = clean_text(node.text_content())
        if not text:
            return None
        if title:
            text = clean_text(text.replace(title, "", 1))
        return text
