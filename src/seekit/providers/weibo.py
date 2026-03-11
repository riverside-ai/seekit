from ._base import BaseSERP, SerpItem, extract_json_from_text, strip_html


class WeiboSerp(BaseSERP):
    provider = "weibo"

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
