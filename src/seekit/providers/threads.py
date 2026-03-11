from ._base import BaseSERP, SerpItem, extract_json_from_text, take_text


class ThreadsSerp(BaseSERP):
    provider = "threads"

    def pick_entry(self, entries: list[dict[str, object]]) -> dict[str, object]:
        return entries[-1]

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        root = payload["data"].get("searchResults", {})
        items: list[SerpItem] = []
        for edge in root.get("edges", []):
            thread = edge["node"]["thread"]
            post = thread["thread_items"][0]["post"]
            user = post.get("user", {})
            title = take_text(post.get("text_post_app_info", {}).get("text_fragments"))
            built = self.make_item(
                title=title,
                excerpt=title,
                url=post.get("canonical_url"),
                author=user.get("username") or user.get("full_name"),
                cover_url=user.get("profile_pic_url"),
            )
            if built is not None:
                items.append(built)
        return items
