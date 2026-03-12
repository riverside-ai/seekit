from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text, take_text


class YouTubeSerp(BaseSERP):
    provider = "youtube"
    request_template = build_request_template(
        method="GET",
        url="https://www.youtube.com/results?search_query=OpenClaw",
        headers={
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "device-memory": "8",
            "sec-ch-dpr": "2",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-arch": "\"arm\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-form-factors": "\"Desktop\"",
            "sec-ch-ua-full-version": "\"145.0.7632.160\"",
            "sec-ch-ua-full-version-list": "\"Not:A-Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"145.0.7632.160\", \"Chromium\";v=\"145.0.7632.160\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-ch-ua-platform-version": "\"15.5.0\"",
            "sec-ch-ua-wow64": "?0",
            "sec-ch-viewport-width": "1063",
        },
        cookies={},
    )

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
