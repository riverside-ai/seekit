from typing import Any

from ._base import HtmlSERP, SerpItem


class GoogleSerp(HtmlSERP):
    provider = "google"
    base_url = "https://www.google.com"
    item_xpath = '//div[@class="MjjYud"][.//div[@class="yuRUbf"]//a[@href]]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, './/div[@class="yuRUbf"]//h3[1]')
        url = self.first_attr(node, './/div[@class="yuRUbf"]//a[@href][1]/@href')
        author = self.first_text(node, './/span[contains(@class,"VuuXrf")][1]')
        excerpt = self.first_text(
            node,
            './/*[contains(@class,"VwiC3b")][1]',
            './/*[contains(@class,"yXK7lf")][1]',
        ) or self.fallback_excerpt(node, title)
        return self.make_item(
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
            base_url=self.base_url,
        )
