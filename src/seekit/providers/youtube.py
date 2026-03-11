from ._base import BaseSERP, SerpItem, extract_json_from_text, take_text


class YouTubeSerp(BaseSERP):
    provider = "youtube"

    def parse_response(self, body: str) -> list[SerpItem]:
        marker = "var ytInitialData = "
        start = body.find(marker)
        if start == -1:
            return []
        payload = extract_json_from_text(body[start + len(marker) :])
        sections = payload["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"]
        items: list[SerpItem] = []
        for section in sections:
            renderer = section.get("itemSectionRenderer")
            if not renderer:
                continue
            for entry in renderer["contents"]:
                video = entry.get("videoRenderer")
                if not video:
                    continue
                thumbnails = video.get("thumbnail", {}).get("thumbnails") or []
                item = self.make_item(
                    title=take_text(video.get("title")),
                    excerpt=take_text(video.get("detailedMetadataSnippets")),
                    url="https://www.youtube.com/watch?v=" + video["videoId"],
                    author=take_text(video.get("ownerText"))
                    or take_text(video.get("longBylineText")),
                    cover_url=thumbnails[-1].get("url") if thumbnails else None,
                )
                if item is not None:
                    items.append(item)
        return items
