from typing import Any

from ._base import HtmlSERP, SerpItem


class BraveSerp(HtmlSERP):
    provider = "brave"
    item_xpath = '//div[@id="results"]//div[@data-type="web"]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, './/div[contains(@class,"title")][1]')
        url = self.first_attr(node, ".//a[@href][1]/@href")
        author = self.first_text(node, './/div[contains(@class,"site-name-content")]//div[1]')
        cover_url = self.first_attr(node, './/img[contains(@class,"favicon")][1]/@src')
        excerpt = self.first_text(
            node,
            './/div[contains(@class,"generic-snippet")]//*[contains(@class,"content")][1]',
            './/div[contains(@class,"description")][1]',
        ) or self.fallback_excerpt(node, title)
        return self.make_item(
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
            cover_url=cover_url,
        )
