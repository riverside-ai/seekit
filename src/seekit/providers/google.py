from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class GoogleSerp(HtmlSERP):
    provider = "google"
    base_url = "https://www.google.com"
    request_template = build_request_template(
        method="GET",
        url="https://www.google.com/search?q=OpenClaw&num=10&sca_esv=8029562fbebb207c&sxsrf=ANbL-n455Oq0zLdvs7rR2kqwwQ4lLpBQiQ%3A1773210342838&source=hp&ei=5gqxaZ7FMYWc0-kP_LzDmA4&iflsig=AFdpzrgAAAAAabEY9g-In36PzqCDEIi7kIFCaF2P_fgc&ved=0ahUKEwie0OGkm5eTAxUFzjQHHXzeEOMQ4dUDCB4&uact=5&oq=OpenClaw&gs_lp=Egdnd3Mtd2l6IghPcGVuQ2xhdzIEECMYJzIEECMYJzIEECMYJzIKEAAYgAQYFBiHAjIKEAAYgAQYigUYQzIKEAAYgAQYigUYQzIKEAAYgAQYigUYQzIKEAAYgAQYigUYQzIKEAAYgAQYigUYQzIHEAAYgAQYCkiEUVDcGVjyLHAFeACQAQCYAd8BoAGdEaoBBTAuNi41uAEDyAEA-AEBmAIQoALcEagCCsICBxAjGOoCGCfCAgUQABiABMICCxAuGIAEGMcBGNEDwgILEAAYgAQYigUYkQLCAgkQABiABBgKGAuYAwXxBVmWPJPE0gIwkgcFNS42LjWgB85PsgcFMC42LjW4B8sRwgcGMC4xMi40yAcqgAgB&sclient=gws-wiz",
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd, dcb, dcz",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "available-dictionary": ":srt/L7zZa4TX3VS/9/JtgDcg7u0FHl5rl/6Pb0L3KUA=:",
            "cache-control": "no-cache",
            "downlink": "8.1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.google.com/",
            "rtt": "250",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-arch": "\"arm\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-form-factors": "\"Desktop\"",
            "sec-ch-ua-full-version": "\"145.0.7632.160\"",
            "sec-ch-ua-full-version-list": "\"Not:A-Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"145.0.7632.160\", \"Chromium\";v=\"145.0.7632.160\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-ch-ua-platform-version": "\"15.5.0\"",
            "sec-ch-ua-wow64": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-browser-channel": "stable",
            "x-browser-copyright": "Copyright 2026 Google LLC. All Rights reserved.",
            "x-browser-validation": "lbZsdhRUx3IBWze7ecNtqg7Djq0=",
            "x-browser-year": "2026",
            "x-client-data": "CISCywE=",
        },
        cookies={},
    )
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
