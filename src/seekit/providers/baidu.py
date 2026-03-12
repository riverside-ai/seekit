from typing import Any

from ._base import HtmlSERP, SerpItem, build_request_template


class BaiduSerp(HtmlSERP):
    provider = "baidu"
    request_template = build_request_template(
        method="GET",
        url="https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=92CE26733D323945&ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=OpenClaw&fenlei=256&rsv_pq=0x9670b831004ea345&rsv_t=3ae20OHGlExqjnXiNAEryfJxos8Y9Jc0kBir0E97510nSY2Uq8cAhCp62gRI&rqlang=en&rsv_dl=tb&rsv_enter=1&rsv_sug3=13&rsv_sug1=3&rsv_sug7=101&rsv_btype=i&prefixsug=Open%2526lt%253Blaw&rsp=3&inputT=3321&rsv_sug4=3976&rsv_sug=1&rsv_sid=60272_63145_67078_67494_67754_67862_67884_67886_67946_67951_67954_67956_67964_68048_68076_68081_68099_67985_68002_68125_68136_68142_68149_68151_68139_68165_68193_68208_68229_68241&_ss=1&clist=&hsug=openclaw&f4s=1&csor=8&_cr1=44936",
        headers={
            "Host": "www.baidu.com",
            "Ps-Dataurlconfigqid": "0x9670b831004ea345",
            "Referer": "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=OpenClaw&fenlei=256&rsv_pq=0x9670b831004ea345&rsv_t=3ae20OHGlExqjnXiNAEryfJxos8Y9Jc0kBir0E97510nSY2Uq8cAhCp62gRI&rqlang=en&rsv_dl=tb&rsv_enter=1&rsv_sug3=13&rsv_sug1=3&rsv_sug7=101&rsv_btype=i&prefixsug=Open%2526lt%253Blaw&rsp=3&inputT=3321&rsv_sug4=3976&rsv_sug=1",
            "X-Requested-With": "XMLHttpRequest",
            "is_referer": "https://www.baidu.com/",
            "is_xhr": "1",
        },
        cookies={},
    )
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
