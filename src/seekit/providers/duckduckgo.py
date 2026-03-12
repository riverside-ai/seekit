import json
import re

from ._base import BaseSERP, SerpItem, build_request_template, clean_text, strip_html


class DuckDuckGoSerp(BaseSERP):
    provider = "duckduckgo"
    request_template = build_request_template(
        method="GET",
        url="https://duckduckgo.com/?ia=web&origin=funnel_home_website&t=h_&q=OpenClaw&chip-select=search",
        headers={
            "referer": "https://duckduckgo.com/",
        },
        cookies={},
    )

    def parse_response(self, body: str) -> list[SerpItem]:
        match = re.search(r"DDG\.duckbar\.add\((\{.*?\}),null,\"index\"\)", body)
        if not match:
            return []
        payload = json.loads(match.group(1))
        abstract = clean_text(payload["data"].get("AbstractText"))
        items: list[SerpItem] = []
        for result in payload["data"].get("Results", []):
            item = self.make_item(
                title=strip_html(result.get("Text")),
                excerpt=abstract,
                url=result.get("FirstURL"),
                author=payload["data"].get("AbstractSource"),
                cover_url=result.get("Icon", {}).get("URL"),
            )
            if item is not None:
                items.append(item)
        return items
