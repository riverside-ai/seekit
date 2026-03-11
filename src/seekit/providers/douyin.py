import json

from ._base import BaseSERP, SerpItem, extract_json_from_text


class DouyinSerp(BaseSERP):
    provider = "douyin"

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        items: list[SerpItem] = []
        for card in payload.get("data", []):
            for sub_card in card.get("sub_card_list", []):
                display = sub_card.get("common_aladdin", {}).get("display")
                if not display:
                    continue
                content = json.loads(display)
                hotspot = content.get("hotspot_info") or {}
                item = self.make_item(
                    title=hotspot.get("sentence"),
                    excerpt=hotspot.get("desc"),
                    url=hotspot.get("schema"),
                    author=hotspot.get("header"),
                    cover_url=(hotspot.get("board_icon") or {}).get("light"),
                )
                if item is not None:
                    items.append(item)
        return items
