from __future__ import annotations

import argparse
import csv
from collections.abc import Sequence
import json
from pathlib import Path
from io import StringIO
from string import Template
import sys
import textwrap

from rich.console import Console
from rich.markdown import Heading, Markdown
from rich.table import Table

Heading.LEVEL_ALIGN["h1"] = "left"

from . import PROVIDERS, SerpItem, get_provider

TEMPLATE_PATH = Path(__file__).parent / "serp.md.template"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seekit",
        description="Search a provider and print normalized results.",
    )
    parser.add_argument("keyword", nargs="+", help="Search keyword")
    parser.add_argument(
        "--engine",
        choices=sorted(PROVIDERS),
        default="bing",
        help="Search engine to use (default: bing)",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "table", "json", "csv"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of rows to print (default: 10)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Raise exceptions and save the raw response body for debugging",
    )
    return parser


def truncate(value: str | None, width: int) -> str:
    text = (value or "").strip()
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."


def build_table(items: Sequence[SerpItem]) -> Table:
    table = Table(title="seekit results", show_lines=False)
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Provider", style="magenta")
    table.add_column("Title", style="bold")
    table.add_column("Author")
    table.add_column("Time")
    table.add_column("URL", overflow="fold")
    for index, item in enumerate(items, start=1):
        table.add_row(
            str(index),
            item.provider,
            truncate(item.title, 42),
            truncate(item.author, 18),
            truncate(item.time, 18),
            truncate(item.url, 60),
        )
    return table


def serialize_items(items: Sequence[SerpItem]) -> list[dict[str, str | None]]:
    return [item.model_dump(mode="json") for item in items]


def format_json(items: Sequence[SerpItem]) -> str:
    return json.dumps(serialize_items(items), indent=2, ensure_ascii=False)


def format_csv(items: Sequence[SerpItem]) -> str:
    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["provider", "title", "excerpt", "url", "author", "cover_url", "time"],
    )
    writer.writeheader()
    for row in serialize_items(items):
        writer.writerow(row)
    return output.getvalue().rstrip("\n")


def format_detail(items: Sequence[SerpItem]) -> str:
    blocks: list[str] = []
    for index, item in enumerate(items, start=1):
        lines = [
            f"[{index}] {item.title or '(no title)'}",
            f"provider: {item.provider}",
        ]
        if item.author:
            lines.append(f"author: {item.author}")
        if item.url:
            lines.append(f"url: {item.url}")
        if item.time:
            lines.append(f"time: {item.time}")
        if item.excerpt:
            lines.append("excerpt:")
            lines.extend(textwrap.wrap(item.excerpt, width=100))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _format_md_item(index: int, item: SerpItem) -> str:
    title = item.title or "(no title)"
    lines = [f"## {index}. {title}", ""]
    if item.url:
        lines.append(f"**URL:** {item.url}  ")
    if item.author:
        lines.append(f"**Author:** {item.author}  ")
    if item.time:
        lines.append(f"**Time:** {item.time}  ")
    if item.excerpt:
        lines.append("")
        lines.append(item.excerpt)
    return "\n".join(lines)


def format_markdown(items: Sequence[SerpItem], keyword: str, engine: str) -> str:
    result_blocks = "\n\n".join(
        _format_md_item(i, item) for i, item in enumerate(items, start=1)
    )
    template_text = TEMPLATE_PATH.read_text()
    return Template(template_text).safe_substitute(
        keyword=keyword, engine=engine, results=result_blocks
    )


def _save_debug(engine: str, keyword: str, provider: object, body: str | None, err_console: Console) -> None:
    from .providers._base import RequestTemplate

    cwd = Path.cwd()
    if body is not None:
        html_path = cwd / f"seekit-{engine}-debug.html"
        html_path.write_text(body)
        err_console.print(f"[yellow]Saved response to {html_path}[/yellow]")

    template: RequestTemplate | None = None
    try:
        template = provider.get_request_template(keyword)  # type: ignore[attr-defined]
    except Exception:
        pass

    if template is not None:
        lines = [
            f"# Debug: seekit {engine}",
            "",
            f"**Keyword:** {keyword}",
            "",
            "## Request",
            "",
            f"**Method:** {template.method}  ",
            f"**URL:** {template.url}",
            "",
            "### Headers",
            "",
        ]
        for name, value in template.headers.items():
            lines.append(f"- `{name}`: `{value}`")
        if template.cookies:
            lines.append("")
            lines.append("### Cookies")
            lines.append("")
            for name, value in template.cookies.items():
                lines.append(f"- `{name}`: `{value}`")
        if template.body:
            lines.append("")
            lines.append("### Body")
            lines.append("")
            lines.append("```")
            lines.append(template.body)
            lines.append("```")
        md_path = cwd / f"seekit-{engine}-debug.md"
        md_path.write_text("\n".join(lines) + "\n")
        err_console.print(f"[yellow]Saved request metadata to {md_path}[/yellow]")


def main(argv: Sequence[str] | None = None) -> int:
    console = Console()
    err_console = Console(stderr=True)
    parser = build_parser()
    args = parser.parse_args(argv)
    keyword = " ".join(args.keyword)
    provider = get_provider(args.engine)
    body: str | None = None

    try:
        body = provider.request(keyword)
        results = provider.parse_response(body)
    except Exception as exc:
        if args.debug:
            _save_debug(args.engine, keyword, provider, body, err_console)
            raise
        print(f"seekit: {exc}", file=sys.stderr)
        return 1

    if args.debug:
        _save_debug(args.engine, keyword, provider, body, err_console)

    if args.limit < 1:
        print("seekit: --limit must be at least 1", file=sys.stderr)
        return 2

    items = results[: args.limit]
    if not items:
        print("No results.")
        return 0

    if args.format == "json":
        print(format_json(items))
        return 0

    if args.format == "csv":
        print(format_csv(items))
        return 0

    if args.format == "table":
        console.print(build_table(items))
        console.print()
        console.print(format_detail(items))
        return 0

    md_text = format_markdown(items, keyword, args.engine)
    if console.is_terminal:
        console.print(Markdown(md_text))
    else:
        print(md_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
