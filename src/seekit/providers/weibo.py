from __future__ import annotations

"""
The fix turned out to be simple — we were calling passport.weibo.com but the
browser uses visitor.passport.weibo.cn. The correct visitor flow is:

1. GET visitor.passport.weibo.cn/visitor/genvisitor2 → get tid
2. GET visitor.passport.weibo.cn/visitor/visitor?a=incarnate&t=<tid>... →
get SUB/SUBP
3. Set cookies on .weibo.cn, visit m.weibo.cn → get XSRF-TOKEN
4. Search API with x-xsrf-token header

The session is cached (@cache) so the visitor flow only runs once per
process.
"""

import json
from functools import cache

import curl_cffi
import curl_cffi.requests

from ._base import BaseSERP, RequestTemplate, SerpItem, extract_json_from_text, strip_html


@cache
def _get_weibo_session() -> curl_cffi.requests.Session:
    """Obtain a valid visitor session for m.weibo.cn via the passport flow."""
    s = curl_cffi.requests.Session(impersonate="chrome")

    # Step 1: Get visitor identity from visitor.passport.weibo.cn
    resp = s.get(
        "https://visitor.passport.weibo.cn/visitor/genvisitor2",
        params={"cb": "gen_callback", "fp": "{}"},
        headers={"referer": "https://visitor.passport.weibo.cn/"},
    )
    text = resp.text
    payload = json.loads(text[text.index("{") : text.rindex("}") + 1])
    tid = payload["data"]["tid"]

    # Step 2: Incarnate to get SUB/SUBP cookies
    resp2 = s.get(
        "https://visitor.passport.weibo.cn/visitor/visitor",
        params={
            "a": "incarnate",
            "t": tid,
            "w": "2",
            "c": "095",
            "cb": "cross_domain",
            "from": "sinawap",
            "url": "https://m.weibo.cn/search?containerid=231583",
            "domain": ".weibo.cn",
        },
        headers={"referer": "https://visitor.passport.weibo.cn/"},
    )
    text2 = resp2.text
    data = json.loads(text2[text2.index("{") : text2.rindex("}") + 1])

    # Step 3: Create a clean session with cookies on .weibo.cn
    session = curl_cffi.requests.Session(impersonate="chrome")
    session.cookies.set("SUB", data["data"]["sub"], domain=".weibo.cn")
    session.cookies.set("SUBP", data["data"]["subp"], domain=".weibo.cn")

    # Step 4: Visit the page to obtain XSRF-TOKEN
    session.get(
        "https://m.weibo.cn/search?containerid=231583",
        headers={"accept": "text/html"},
    )
    return session


class WeiboSerp(BaseSERP):
    provider = "weibo"
    request_template = RequestTemplate(
        method="GET",
        url="https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D$keyword_plus&page_type=searchall",
        headers={
            "x-requested-with": "XMLHttpRequest",
            "mweibo-pwa": "1",
            "accept": "application/json, text/plain, */*",
            "referer": "https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D$keyword_plus",
        },
        cookies={},
    )

    def request(self, keyword: str) -> str:
        template = self.get_request_template(keyword)
        session = _get_weibo_session()
        xsrf = dict(session.cookies).get("XSRF-TOKEN", "")
        headers = {
            **template.headers,
            "x-xsrf-token": xsrf,
        }
        headers = {k: v for k, v in headers.items() if k.lower() != "content-length"}
        response = session.get(
            template.url,
            headers=headers,
        )
        return response.text

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        items: list[SerpItem] = []
        for card in payload["data"].get("cards", []):
            if card.get("card_type") != 9:
                continue
            post = card["mblog"]
            user = post.get("user", {})
            built = self.make_item(
                title=strip_html(post.get("text")),
                excerpt=strip_html(post.get("text")),
                url=f"https://m.weibo.cn/detail/{post['id']}",
                author=user.get("screen_name"),
                cover_url=user.get("profile_image_url"),
            )
            if built is not None:
                items.append(built)
        return items
