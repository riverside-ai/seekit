from typing import Any

from ._base import HtmlSERP, SerpItem


class RedditSerp(HtmlSERP):
    provider = "reddit"
    base_url = "https://www.reddit.com"
    item_xpath = '//a[@data-testid="post-title-text"]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, ".")
        url = self.first_attr(node, "./@href")
        excerpt = self.first_text(
            node.getparent(),
            './/a[contains(@class,"line-clamp-2")][1]',
        )
        author = self.first_text(
            node.getparent(),
            './/a[starts-with(@href,"/r/")][1]',
        )
        return self.make_item(
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
            base_url=self.base_url,
        )
