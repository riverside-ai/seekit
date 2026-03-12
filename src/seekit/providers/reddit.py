from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class RedditSerp(HtmlSERP):
    provider = "reddit"
    base_url = "https://www.reddit.com"
    request_template = build_request_template(
        method="GET",
        url="https://www.reddit.com/search/?q=OpenClaw&cId=a4b7958c-599f-4021-8477-ad4e53afe558&iId=6d1de8a1-657c-4731-b8f4-ed06c8b712f8",
        headers={
            "clienthash": "Hq0G2sb7iXxQMj2a",
            "nonce": "qwArlBEgf8Learlts34AiQ==",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.reddit.com/",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        },
        cookies={},
    )
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
