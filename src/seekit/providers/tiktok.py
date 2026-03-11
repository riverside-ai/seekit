from ._base import BaseSERP, SerpItem, extract_json_from_text


class TiktokSerp(BaseSERP):
    provider = "tiktok"

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        items: list[SerpItem] = []
        for entry in payload.get("data", []):
            item = entry.get("item")
            if not item:
                continue
            author = item.get("author", {})
            unique_id = author.get("uniqueId")
            video_id = item.get("id")
            url = None
            if unique_id and video_id:
                url = f"https://www.tiktok.com/@{unique_id}/video/{video_id}"
            excerpt = item.get("desc") or author.get("signature")
            built = self.make_item(
                title=item.get("desc") or author.get("nickname"),
                excerpt=excerpt,
                url=url,
                author=author.get("nickname") or unique_id,
                cover_url=item.get("video", {}).get("cover"),
            )
            if built is not None:
                items.append(built)
        return items
