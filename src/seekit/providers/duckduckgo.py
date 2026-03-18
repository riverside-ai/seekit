from typing import Any
from urllib.parse import urlparse, parse_qs

from ._base import HtmlSERP, SerpItem, RequestTemplate


class DuckDuckGoSerp(HtmlSERP):
    provider = "duckduckgo"
    base_url = "https://html.duckduckgo.com"
    request_template = RequestTemplate(
        method="GET",
        url="https://html.duckduckgo.com/html/?q=$keyword_plus",
        headers={
            "referer": "https://html.duckduckgo.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        },
        cookies={},
    )
    item_xpath = '//div[contains(@class,"web-result")]'

    @staticmethod
    def _extract_url(raw: str | None) -> str | None:
        """Extract the actual URL from a DDG redirect link."""
        if not raw:
            return None
        uddg = parse_qs(urlparse(raw).query).get("uddg")
        if uddg:
            return uddg[0]
        return raw

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, './/a[@class="result__a"][1]')
        raw_url = self.first_attr(node, './/a[@class="result__a"][1]/@href')
        url = self._extract_url(raw_url)
        excerpt = self.first_text(node, './/*[contains(@class,"result__snippet")][1]')
        author = self.first_text(node, './/*[contains(@class,"result__url")][1]')
        return self.make_item(
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
        )
