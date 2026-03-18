from __future__ import annotations

import base64
from dataclasses import dataclass
from functools import cache
import json
from pathlib import Path
from typing import Any

from urllib.parse import quote, quote_plus, urlsplit, urlunsplit

import yaml

KEYWORD_PLACEHOLDER = "OpenClaw"


@dataclass(frozen=True)
class EngineExample:
    keyword: str
    page: str


@dataclass(frozen=True)
class EngineConfig:
    name: str
    example: EngineExample
    type: str | None = None
    entry_index: int = 0


@cache
def load_engine_configs(path: str | Path | None = None) -> tuple[EngineConfig, ...]:
    source = Path(path) if path is not None else Path("data/info.yaml")
    with source.open() as handle:
        payload = yaml.safe_load(handle)
    configs = []
    for entry in payload["engines"]:
        if entry.get("disabled"):
            continue
        example = EngineExample(**entry["example"])
        configs.append(EngineConfig(
            name=entry["name"],
            example=example,
            type=entry.get("type"),
            entry_index=entry.get("entry_index", 0),
        ))
    return tuple(configs)


@cache
def load_engine_config_map(path: str | Path | None = None) -> dict[str, EngineConfig]:
    return {config.name: config for config in load_engine_configs(path)}


def get_engine_config(name: str, path: str | Path | None = None) -> EngineConfig:
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


def templatize(value: str, placeholder: str = KEYWORD_PLACEHOLDER) -> str:
    """Replace a literal keyword from a HAR capture with $-style template placeholders."""
    replacements = (
        (quote_plus(placeholder), "$keyword_plus"),
        (quote(placeholder, safe=""), "$keyword_quoted_strict"),
        (quote(placeholder), "$keyword_quoted"),
        (placeholder, "$keyword"),
    )
    result = value
    for source, target in replacements:
        result = result.replace(source, target)
    return result


def templatize_url(url: str, placeholder: str = KEYWORD_PLACEHOLDER) -> str:
    """Convert a HAR-captured URL into a $-style template."""
    parts = urlsplit(url)
    path = templatize(parts.path, placeholder)
    query_parts: list[str] = []
    if parts.query:
        for chunk in parts.query.split("&"):
            if "=" in chunk:
                key, value = chunk.split("=", 1)
                query_parts.append(
                    f"{templatize(key, placeholder)}={templatize(value, placeholder)}"
                )
            else:
                query_parts.append(templatize(chunk, placeholder))
    query = "&".join(query_parts)
    fragment = templatize(parts.fragment, placeholder)
    return urlunsplit((parts.scheme, parts.netloc, path, query, fragment))


def parse_har(provider: str, har_path: str | Path, entry_index: int = 0) -> list[Any]:
    from seekit import get_provider

    parser = get_provider(provider)
    entries = load_har_entries(har_path)
    entry = entries[entry_index]
    body = decode_har_content(entry["response"]["content"])
    return parser.parse_response(body)


PSEUDO_HEADERS = frozenset({":authority", ":method", ":path", ":scheme", ":status"})


def _extract_request_params(
    request: dict[str, Any],
    placeholder: str = KEYWORD_PLACEHOLDER,
) -> dict[str, Any]:
    """Extract and decompose a HAR request entry into structured params."""
    parts = urlsplit(request["url"])
    base_url = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

    query: dict[str, str] = {}
    for item in request.get("queryString", []):
        query[item["name"]] = templatize(item["value"], placeholder)

    headers: dict[str, str] = {}
    for item in request.get("headers", []):
        name = item["name"].lower()
        if name in PSEUDO_HEADERS:
            continue
        headers[name] = templatize(item["value"], placeholder)

    cookies: dict[str, str] = {}
    for item in request.get("cookies", []):
        cookies[item["name"]] = templatize(item["value"], placeholder)

    result: dict[str, Any] = {
        "method": request["method"],
        "url": base_url,
        "query": query,
        "headers": headers,
        "cookies": cookies,
    }

    post_data = request.get("postData")
    if post_data and post_data.get("params"):
        body: dict[str, str] = {}
        for param in post_data["params"]:
            body[param["name"]] = templatize(param["value"], placeholder)
        result["body"] = body

    return result


def generate_params(
    info_path: str | Path | None = None,
    pages_dir: str | Path | None = None,
    output_path: str | Path | None = None,
) -> None:
    """Read info.yaml + HAR files and write params.yaml."""
    root = Path(__file__).resolve().parent
    if info_path is None:
        info_path = root / "info.yaml"
    if pages_dir is None:
        pages_dir = root / "pages"
    if output_path is None:
        output_path = root.parent / "src" / "seekit" / "params.yaml"

    info_path = Path(info_path)
    pages_dir = Path(pages_dir)
    output_path = Path(output_path)

    with info_path.open() as f:
        info = yaml.safe_load(f)

    engines: dict[str, Any] = {}
    for engine_entry in info["engines"]:
        if engine_entry.get("disabled"):
            continue
        name = engine_entry["name"]
        har_file = pages_dir / engine_entry["example"]["page"]
        entry_index = engine_entry.get("entry_index", 0)
        keyword = engine_entry["example"].get("keyword", KEYWORD_PLACEHOLDER)

        entries = load_har_entries(har_file)
        entry = entries[entry_index]
        params = _extract_request_params(entry["request"], keyword)
        engines[name] = params

    with output_path.open("w") as f:
        yaml.dump({"engines": engines}, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Generated {output_path} with {len(engines)} engines")


if __name__ == "__main__":
    generate_params()
