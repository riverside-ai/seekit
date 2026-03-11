# ruff: noqa: E501
from curl_cffi import requests

from .base import BaseSERP


class QihooSERP(BaseSERP):
    CONTENT_XPATH = './/li[@class="res-list"]'
    AD_XPATH = './/span[text()="广告"]'

    def request(self, keyword: str):
        response = requests.get(
            url="https://www.so.com/s",
            impersonate="chrome120",
            params={
                "ie": "utf-8",
                "fr": "360sou_newhome",
                "src": "home_so.360.cn",
                "ssid": "881d00c1f3c24afbb57c88c771b90541",
                "sp": "ab6",
                "cp": "08e0032ad8",
                "nlpv": "placeholder_base_dt_60",
                "q": keyword,
            },
            headers={
                # type: ignore
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "DNT": "1",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
            },
            cookies={
                # type: ignore
                "QiHooGUID": "DE0CD9CE1C57D76DEB8F416BF4CE2115.1740035171783; __guid=15484592.297570284909470400.1740035174887.8137; so-like-red=2; webp=1; so_huid=11PRUS7dh978S1hHR8khDWtPSQz8V1Bt6cPHR9fATieYk%3D; __huid=11PRUS7dh978S1hHR8khDWtPSQz8V1Bt6cPHR9fATieYk%3D; dpr=2; gtHuid=1; WZWS4=0ced2dfa26841bfc5dfe244a627a16ba; _S=8gm2aet088kus1lrrvcegmk057; count=3; erules=p2-3%7Ckd-5"
            },
        )
        return response.text

    def _clean(self, tree):
        for a_tag in tree.xpath('//a[contains(@href, "e.so.com")]'):
            a_tag.getparent().remove(a_tag)


if __name__ == "__main__":
    # dotenv run python -m rag.serp.qihoo
    serp = QihooSERP()
    # serp.test_file("./data/serp/qihoo_clean.html")
    serp.test_query("北京天气")
