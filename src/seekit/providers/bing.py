from typing import Any

from ._base import HtmlSERP, SerpItem


class BingSerp(HtmlSERP):
    provider = "bing"
    item_xpath = '//li[contains(concat(" ", normalize-space(@class), " "), " b_algo ")]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, ".//h2[1]")
        url = self.first_attr(node, ".//h2[1]/a/@href")
        author = self.first_text(node, './/div[contains(@class,"tptt")][1]')
        excerpt = self.first_text(node, './/div[contains(@class,"b_caption")]//p[1]')
        return self.make_item(title=title, excerpt=excerpt, url=url, author=author)
