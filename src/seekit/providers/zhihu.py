from __future__ import annotations

import hashlib
import subprocess
from functools import cache
from pathlib import Path
from urllib.parse import quote_plus, urlparse

import curl_cffi
import curl_cffi.requests

from ._base import BaseSERP, SerpItem, extract_json_from_text, strip_html

_JS_PATH = str(Path(__file__).parent.parent / "zhihu_encrypt.js")
_ZSE_93 = "101_3_2.0"


@cache
def _get_zhihu_session() -> curl_cffi.requests.Session:
    """Obtain a session with a valid d_c0 cookie via the /udid endpoint."""
    s = curl_cffi.requests.Session(impersonate="chrome")
    s.post(
        "https://www.zhihu.com/udid",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    if "d_c0" not in dict(s.cookies):
        raise RuntimeError("Failed to obtain d_c0 cookie from zhihu.com")
    return s


def _get_dc0(session: curl_cffi.requests.Session) -> str:
    """Extract the d_c0 cookie value from the session."""
    return dict(session.cookies)["d_c0"]


def _encrypt(md5_hex: str) -> str:
    """Call the Node.js encrypt function to produce the x-zse-96 payload."""
    result = subprocess.run(
        ["node", _JS_PATH, md5_hex],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(f"zhihu encrypt failed: {result.stderr}")
    return result.stdout.strip()


def _sign(url_path: str, dc0: str) -> str:
    """Generate x-zse-96 header value."""
    plaintext = "+".join([_ZSE_93, url_path, dc0])
    md5_hex = hashlib.md5(plaintext.encode()).hexdigest()
    encrypted = _encrypt(md5_hex)
    return f"2.0_{encrypted}"


class ZhihuSerp(BaseSERP):
    provider = "zhihu"

    def request(self, keyword: str) -> str:
        session = _get_zhihu_session()
        dc0 = _get_dc0(session)

        params = {
            "t": "general",
            "q": keyword,
            "correction": "1",
            "offset": "0",
            "limit": "20",
            "filter_fields": "",
            "lc_idx": "0",
            "show_all_topics": "0",
            "search_source": "Normal",
        }
        query_string = "&".join(f"{k}={quote_plus(str(v))}" for k, v in params.items())
        url = f"https://www.zhihu.com/api/v4/search_v3?{query_string}"
        url_path = urlparse(url).path + "?" + urlparse(url).query

        x_zse_96 = _sign(url_path, dc0)

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "referer": f"https://www.zhihu.com/search?type=content&q={quote_plus(keyword)}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-api-version": "3.0.91",
            "x-app-za": "OS=Web",
            "x-requested-with": "fetch",
            "x-zse-93": _ZSE_93,
            "x-zse-96": x_zse_96,
        }
        headers = {k: v for k, v in headers.items() if k.lower() != "content-length"}

        response = session.get(url, headers=headers)
        return response.text

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        items: list[SerpItem] = []
        for result in payload.get("data", []):
            if result.get("type") != "search_result":
                continue
            obj = result["object"]
            thumbnails = obj.get("thumbnail_info", {}).get("thumbnails") or []
            built = self.make_item(
                title=obj.get("title") or strip_html(obj.get("content")),
                excerpt=strip_html(obj.get("excerpt")) or strip_html(obj.get("content")),
                url=obj.get("url"),
                author=obj.get("author", {}).get("name"),
                cover_url=thumbnails[0].get("url") if thumbnails else None,
            )
            if built is not None:
                items.append(built)
        return items
