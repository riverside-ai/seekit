from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class YandexSerp(HtmlSERP):
    provider = "yandex"
    request_template = build_request_template(
        method="GET",
        url="https://yandex.com/search/?text=OpenClaw&lr=10636&msid=1773212892743375-13893706528193923191-balancer-l7leveler-kubr-yp-klg-259-BAL&search_source=yacom_desktop_common&suggest_reqid=993923191177321289228939199850110",
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "device-memory": "8",
            "downlink": "10",
            "dpr": "2",
            "ect": "4g",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://yandex.com/",
            "rtt": "150",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-arch": "\"arm\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-full-version": "\"145.0.7632.160\"",
            "sec-ch-ua-full-version-list": "\"Not:A-Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"145.0.7632.160\", \"Chromium\";v=\"145.0.7632.160\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-ch-ua-platform-version": "\"15.5.0\"",
            "sec-ch-ua-wow64": "?0",
            "sec-ch-viewport-height": "897",
            "sec-ch-viewport-width": "1063",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "viewport-width": "1063",
        },
        cookies={},
    )
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
