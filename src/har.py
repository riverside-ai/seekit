from __future__ import annotations

import base64
from dataclasses import dataclass
from functools import cache
import json
from pathlib import Path
from typing import Any

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


@cache
def load_engine_configs(path: str | Path | None = None) -> tuple[EngineConfig, ...]:
    source = Path(path) if path is not None else Path("data/info.yaml")
    with source.open() as handle:
        payload = yaml.safe_load(handle)
    configs = []
    for entry in payload["engines"]:
        example = EngineExample(**entry["example"])
        configs.append(EngineConfig(name=entry["name"], example=example, type=entry.get("type")))
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


def parse_har(provider: str, har_path: str | Path) -> list[Any]:
    from seekit import get_provider

    parser = get_provider(provider)
    entries = load_har_entries(har_path)
    entry = parser.pick_entry(entries)
    body = decode_har_content(entry["response"]["content"])
    return parser.parse_response(body)
