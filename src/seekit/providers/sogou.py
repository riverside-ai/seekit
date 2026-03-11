from typing import Any

from ._base import HtmlSERP, SerpItem


class SogouSerp(HtmlSERP):
    provider = "sogou"
    item_xpath = '//div[@id="main"]//div[contains(@class,"vrwrap") and .//h3//a[@href]]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, ".//h3[1]")
        url = self.first_attr(node, ".//h3//a[1]/@href")
        author = self.first_text(node, ".//cite[1]")
        cover_url = self.first_attr(node, ".//img[1]/@src")
        excerpt = self.first_text(
            node,
            './/*[contains(@class,"str-text-info")][1]',
            ".//p[1]",
        ) or self.fallback_excerpt(node, title)
        return self.make_item(
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
            cover_url=cover_url,
        )
