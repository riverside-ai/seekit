from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class BingSerp(HtmlSERP):
    provider = "bing"
    request_template = build_request_template(
        method="GET",
        url="https://www.bing.com/search?q=OpenClaw&form=QBLH&sp=-1&ghc=1&lq=0&pq=openclaw&sc=12-8&qs=n&sk=&cvid=220EAFC6E29143B9B3C83DBB7DE79851",
        headers={
            "ect": "3g",
            "referer": "https://www.bing.com/?FORM=Z9FD1",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-arch": "\"arm\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-full-version": "\"145.0.7632.160\"",
            "sec-ch-ua-full-version-list": "\"Not:A-Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"145.0.7632.160\", \"Chromium\";v=\"145.0.7632.160\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform-version": "\"15.5.0\"",
        },
        cookies={},
    )
    item_xpath = '//li[contains(concat(" ", normalize-space(@class), " "), " b_algo ")]'

    def parse_node(self, node: Any) -> SerpItem | None:
        title = self.first_text(node, ".//h2[1]")
        url = self.first_attr(node, ".//h2[1]/a/@href")
        author = self.first_text(node, './/div[contains(@class,"tptt")][1]')
        excerpt = self.first_text(node, './/div[contains(@class,"b_caption")]//p[1]')
        return self.make_item(title=title, excerpt=excerpt, url=url, author=author)
