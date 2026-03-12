from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class SoSerp(HtmlSERP):
    provider = "so"
    request_template = build_request_template(
        method="GET",
        url="https://www.so.com/s?q=OpenClaw&src=360portal&_re=0",
        headers={},
        cookies={},
    )
    item_xpath = '//li[contains(@class,"res-list")]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, ".//h3[1]")
        url = self.first_attr(node, ".//h3//a[1]/@href")
        author = self.first_text(node, ".//cite[1]")
        excerpt = self.first_text(node, './/p[contains(@class,"res-desc")][1]', ".//p[1]")
        return self.make_item(title=title, excerpt=excerpt, url=url, author=author)
