import json

from seekit.cli import build_parser, format_csv, format_json
from seekit.providers._base import SerpItem


def sample_items() -> list[SerpItem]:
    return [
        SerpItem(
            provider="bing",
            title="OpenAI",
            excerpt="Model update",
            url="https://example.com/openai",
            author="OpenAI",
            cover_url="https://example.com/image.png",
            time="2026-03-12",
        )
    ]


def test_cli_defaults_to_bing_table_output() -> None:
    args = build_parser().parse_args(["OpenAI"])

    assert args.engine == "bing"
    assert args.format == "table"
    assert args.keyword == ["OpenAI"]


def test_cli_supports_engine_and_format_options() -> None:
    args = build_parser().parse_args(["latest", "OpenAI", "--engine", "baidu", "--format", "json"])

    assert args.engine == "baidu"
    assert args.format == "json"
    assert args.keyword == ["latest", "OpenAI"]


def test_format_json_serializes_items() -> None:
    payload = json.loads(format_json(sample_items()))

    assert payload[0]["provider"] == "bing"
    assert payload[0]["title"] == "OpenAI"


def test_format_csv_serializes_items() -> None:
    payload = format_csv(sample_items())

    assert payload.startswith("provider,title,excerpt,url,author,cover_url,time")
    assert "bing,OpenAI,Model update,https://example.com/openai,OpenAI,https://example.com/image.png,2026-03-12" in payload
