from typing import Any

from ._base import HtmlSERP, SerpItem


class BaiduSerp(HtmlSERP):
    provider = "baidu"
    item_xpath = (
        '//div[@id="content_left"]//div['
        '(contains(@class,"result") or contains(@class,"result-op")) and .//h3//a[@href]'
        "]"
    )

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, ".//h3[1]")
        url = self.first_attr(node, ".//h3//a[1]/@href")
        author = self.first_text(
            node,
            './/*[contains(@class,"cos-tag")][1]',
            './/*[contains(@class,"c-color-gray2")][1]',
        )
        excerpt = self.first_text(
            node,
            './/*[contains(@class,"c-span-last")][1]',
            ".//p[1]",
            ".//div[.//text()][2]",
        ) or self.fallback_excerpt(node, title)
        return self.make_item(title=title, excerpt=excerpt, url=url, author=author)
