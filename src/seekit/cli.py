from __future__ import annotations

import argparse
from collections.abc import Sequence
import sys
import textwrap

from . import PROVIDERS, SerpItem, search


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seekit",
        description="Search a provider and print normalized results in a table.",
    )
    parser.add_argument("provider", choices=sorted(PROVIDERS))
    parser.add_argument("keyword", nargs="+", help="Search keyword")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of rows to print (default: 10)",
    )
    return parser


def truncate(value: str | None, width: int) -> str:
    text = (value or "").strip()
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."


def format_table(items: Sequence[SerpItem]) -> str:
    headers = ("#", "Provider", "Title", "Author", "URL")
    rows = []
    for index, item in enumerate(items, start=1):
        rows.append(
            (
                str(index),
                item.provider,
                truncate(item.title, 42),
                truncate(item.author, 18),
                truncate(item.url, 60),
            )
        )

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    divider = "-+-".join("-" * width for width in widths)
    lines = [
        " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)),
        divider,
    ]
    for row in rows:
        lines.append(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))
    return "\n".join(lines)


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
        if item.excerpt:
            lines.append("excerpt:")
            lines.extend(textwrap.wrap(item.excerpt, width=100))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    keyword = " ".join(args.keyword)

    try:
        results = search(keyword, provider=args.provider)
    except Exception as exc:
        print(f"seekit: {exc}", file=sys.stderr)
        return 1

    if args.limit < 1:
        print("seekit: --limit must be at least 1", file=sys.stderr)
        return 2

    items = results[: args.limit]
    if not items:
        print("No results.")
        return 0

    print(format_table(items))
    print()
    print(format_detail(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
