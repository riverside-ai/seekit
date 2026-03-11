from ._base import BaseSERP, SerpItem, extract_json_from_text, strip_html


class ZhihuSerp(BaseSERP):
    provider = "zhihu"

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
