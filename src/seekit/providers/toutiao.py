import json
import re

import lxml.html

from ._base import BaseSERP, SerpItem, load_request_template, strip_html


class ToutiaoSerp(BaseSERP):
    provider = "toutiao"
    request_template = load_request_template("toutiao")

    def parse_response(self, body: str) -> list[SerpItem]:
        tree = lxml.html.fromstring(body)
        items: list[SerpItem] = []
        for script in tree.xpath("//script"):
            text = (script.text or "").strip()
            if not text.startswith("{") or '"open_url"' not in text:
                continue
            try:
                payload = json.loads(text)
            except (json.JSONDecodeError, ValueError):
                continue
            data = payload.get("data", payload)
            title = strip_html(data.get("title"))
            url = data.get("open_url")
            if not title or not url:
                continue
            built = self.make_item(
                title=title,
                excerpt=strip_html(data.get("abstract")),
                url=url,
                author=data.get("source") or data.get("media_name"),
            )
            if built is not None:
                items.append(built)
        return items
