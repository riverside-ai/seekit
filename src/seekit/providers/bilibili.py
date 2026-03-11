from ._base import BaseSERP, SerpItem, extract_json_from_text, strip_html


class BilibiliSerp(BaseSERP):
    provider = "bilibili"

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        items: list[SerpItem] = []
        for section in payload["data"]["result"]:
            for entry in section.get("data", []):
                if section["result_type"] == "video":
                    url = entry.get("arcurl")
                    title = strip_html(entry.get("title"))
                    excerpt = entry.get("description")
                    author = entry.get("author")
                    cover_url = entry.get("pic")
                elif section["result_type"] == "bili_user":
                    url = f"https://space.bilibili.com/{entry['mid']}"
                    title = entry.get("uname")
                    excerpt = entry.get("usign")
                    author = entry.get("uname")
                    cover_url = entry.get("upic")
                else:
                    continue
                item = self.make_item(
                    title=title,
                    excerpt=excerpt,
                    url=url,
                    author=author,
                    cover_url=cover_url,
                )
                if item is not None:
                    items.append(item)
        return items
