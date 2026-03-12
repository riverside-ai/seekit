from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text, strip_html


class BilibiliSerp(BaseSERP):
    provider = "bilibili"
    request_template = build_request_template(
        method="GET",
        url="https://api.bilibili.com/x/web-interface/wbi/search/all/v2?__refresh__=true&_extra=&context=&page=1&page_size=42&order=&pubtime_begin_s=0&pubtime_end_s=0&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=OpenClaw&qv_id=gTckgRtovmGtKYUYZ0PqzxWq8y3uL8mO&ad_resource=5646&source_tag=3&web_roll_page=1&web_location=1430654&w_rid=85700376544d73302df94d5662c79409&wts=1773209350",
        headers={
            "origin": "https://search.bilibili.com",
            "pragma": "no-cache",
            "referer": "https://search.bilibili.com/all?vt=09333352&keyword=OpenClaw&from_source=webtop_search&spm_id_from=333.1007&search_source=5",
        },
        cookies={},
    )

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
