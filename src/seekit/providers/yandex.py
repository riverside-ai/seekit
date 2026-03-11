from typing import Any

from ._base import HtmlSERP, SerpItem


class YandexSerp(HtmlSERP):
    provider = "yandex"
    item_xpath = '//li[contains(@class,"serp-item")]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(
            node,
            './/*[contains(@class,"OrganicTitleContentSpan")][1]',
            ".//h2[1]",
        )
        url = self.first_attr(node, './/a[contains(@class,"OrganicTitle-Link")][1]/@href')
        excerpt = self.first_text(node, './/*[contains(@class,"OrganicTextContentSpan")][1]')
        author = self.first_text(node, './/*[contains(@class,"OrganicHost-TitleText")][1]')
        return self.make_item(title=title, excerpt=excerpt, url=url, author=author)
