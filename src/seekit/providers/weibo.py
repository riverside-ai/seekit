from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text, strip_html


class WeiboSerp(BaseSERP):
    provider = "weibo"
    request_template = build_request_template(
        method="GET",
        url="https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3DOpenClaw&page_type=searchall",
        headers={
            "sec-ch-ua-platform": "\"macOS\"",
            "X-XSRF-TOKEN": "ffebdd",
            "Referer": "https://m.weibo.cn/search?containerid=100103type%3D1%26q%3DOpenClaw",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "MWeibo-Pwa": "1",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        },
        cookies={},
    )

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
