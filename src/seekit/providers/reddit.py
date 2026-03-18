import json
from typing import Any

from ._base import HtmlSERP, SerpItem, load_request_template


class RedditSerp(HtmlSERP):
    provider = "reddit"
    base_url = "https://www.reddit.com"
    request_template = load_request_template("reddit")
    item_xpath = '//search-telemetry-tracker[.//a[contains(@href,"/comments/")]]'

    def parse_response(self, body: str) -> list[SerpItem]:
        items = super().parse_response(body)
        seen: set[str | None] = set()
        unique: list[SerpItem] = []
        for item in items:
            if item.url not in seen:
                seen.add(item.url)
                unique.append(item)
        return unique

    def parse_node(self, node: Any) -> SerpItem | None:
        ctx_raw = node.get("data-faceplate-tracking-context", "")
        if not ctx_raw:
            return None
        try:
            ctx = json.loads(ctx_raw)
        except (json.JSONDecodeError, ValueError):
            return None

        post = ctx.get("post", {})
        search = ctx.get("search", {})
        subreddit = ctx.get("subreddit", {})

        title = post.get("title")
        excerpt = search.get("snippet") or title
        post_id = (post.get("id") or "").removeprefix("t3_")
        sub_name = subreddit.get("name")

        url = None
        if sub_name and post_id:
            url = f"https://www.reddit.com/r/{sub_name}/comments/{post_id}/"

        author = f"r/{sub_name}" if sub_name else None

        return self.make_item(
            title=title,
            excerpt=excerpt,
            url=url,
            author=author,
        )
