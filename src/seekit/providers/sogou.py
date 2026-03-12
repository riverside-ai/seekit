from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class SogouSerp(HtmlSERP):
    provider = "sogou"
    request_template = build_request_template(
        method="GET",
        url="https://sogou.com/web?query=OpenClaw&_asf=www.sogou.com&_ast=&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index&sourceid=9_01_03&sessiontime=1773211537441",
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "sogou.com",
            "Pragma": "no-cache",
            "Referer": "https://sogou.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
        },
        cookies={},
    )
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
