from __future__ import annotations

from abc import ABC, abstractmethod
import base64
from collections import OrderedDict
from dataclasses import dataclass
from functools import cache
import json
from json import JSONDecoder
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote, quote_plus, urljoin

import curl_cffi
import lxml.html
from pydantic import BaseModel
import yaml


@dataclass(frozen=True)
class EngineExample:
    keyword: str
    page: str


@dataclass(frozen=True)
class EngineConfig:
    name: str
    example: EngineExample
    type: str | None = None


@dataclass(frozen=True)
class HarRequestTemplate:
    method: str
    url: str
    headers: tuple[tuple[str, str], ...]
    cookies: tuple[tuple[str, str], ...]
    body: str | None = None


class SerpItem(BaseModel):
    provider: str
    title: str | None = None
    excerpt: str | None = None
    url: str | None = None
    author: str | None = None
    cover_url: str | None = None


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
def load_engine_configs(path: str | Path = "data/info.yaml") -> tuple[EngineConfig, ...]:
    with Path(path).open() as handle:
        payload = yaml.safe_load(handle)
    configs = []
    for entry in payload["engines"]:
        example = EngineExample(**entry["example"])
        configs.append(EngineConfig(name=entry["name"], example=example, type=entry.get("type")))
    return tuple(configs)


@cache
def load_engine_config_map(path: str | Path = "data/info.yaml") -> dict[str, EngineConfig]:
    return {config.name: config for config in load_engine_configs(path)}


def get_engine_config(name: str, path: str | Path = "data/info.yaml") -> EngineConfig:
    return load_engine_config_map(path)[name]


def load_har_entries(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open() as handle:
        payload = json.load(handle)
    return payload["log"]["entries"]


def decode_har_content(content: dict[str, Any]) -> str:
    text = content.get("text", "")
    if content.get("encoding") == "base64":
        text = base64.b64decode(text).decode("utf-8", errors="ignore")
    return text


def extract_json_from_text(text: str) -> Any:
    candidates = [index for index in (text.find("{"), text.find("[")) if index != -1]
    if not candidates:
        raise ValueError("No JSON payload found in response body.")
    start = min(candidates)
    payload, _ = JSONDecoder().raw_decode(text[start:])
    return payload


def build_har_request_template(entry: dict[str, Any]) -> HarRequestTemplate:
    request = entry["request"]
    headers: list[tuple[str, str]] = []
    for header in request.get("headers", []):
        name = header["name"]
        if name.startswith(":"):
            continue
        headers.append((name, header["value"]))
    cookies = tuple((cookie["name"], cookie["value"]) for cookie in request.get("cookies", []))
    post_data = request.get("postData")
    body = post_data.get("text") if post_data else None
    return HarRequestTemplate(
        method=request["method"],
        url=request["url"],
        headers=tuple(headers),
        cookies=cookies,
        body=body,
    )


def replace_keyword(value: str, source_keyword: str, target_keyword: str) -> str:
    replacements = (
        (source_keyword, target_keyword),
        (quote(source_keyword), quote(target_keyword)),
        (quote(source_keyword, safe=""), quote(target_keyword, safe="")),
        (quote_plus(source_keyword), quote_plus(target_keyword)),
    )
    result = value
    for source, target in replacements:
        result = result.replace(source, target)
    return result


class BaseSERP(ABC):
    provider: str = ""
    base_url: str | None = None

    def get_engine_config(self) -> EngineConfig:
        return get_engine_config(self.provider)

    def get_har_path(self) -> Path:
        config = self.get_engine_config()
        return Path("data/pages") / config.example.page

    def pick_entry(self, entries: list[dict[str, Any]]) -> dict[str, Any]:
        return entries[0]

    def parse_har_file(self, path: str | Path) -> list[SerpItem]:
        entry = self.pick_entry(load_har_entries(path))
        body = decode_har_content(entry["response"]["content"])
        return self.parse_response(body)

    def get_request_template(self, keyword: str) -> HarRequestTemplate:
        config = self.get_engine_config()
        entry = self.pick_entry(load_har_entries(self.get_har_path()))
        template = build_har_request_template(entry)
        return self.apply_keyword_to_template(
            template,
            source_keyword=config.example.keyword,
            target_keyword=keyword,
        )

    def apply_keyword_to_template(
        self,
        template: HarRequestTemplate,
        *,
        source_keyword: str,
        target_keyword: str,
    ) -> HarRequestTemplate:
        return HarRequestTemplate(
            method=template.method,
            url=replace_keyword(template.url, source_keyword, target_keyword),
            headers=template.headers,
            cookies=template.cookies,
            body=(
                replace_keyword(template.body, source_keyword, target_keyword)
                if template.body is not None
                else None
            ),
        )

    def request(self, keyword: str) -> str:
        template = self.get_request_template(keyword)
        response = curl_cffi.requests.request(
            method=template.method,
            url=template.url,
            headers=OrderedDict(template.headers),
            cookies=OrderedDict(template.cookies),
            data=template.body,
            impersonate="chrome120",
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
        base_url: str | None = None,
    ) -> SerpItem | None:
        title = clean_text(title)
        excerpt = clean_text(excerpt)
        author = clean_text(author)
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
