from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text, strip_html


class ZhihuSerp(BaseSERP):
    provider = "zhihu"
    request_template = build_request_template(
        method="GET",
        url="https://www.zhihu.com/api/v4/search_v3?gk_version=gz-gaokao&t=general&q=OpenClaw&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal",
        headers={
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.zhihu.com/search?type=content&q=OpenClaw",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-api-version": "3.0.91",
            "x-app-za": "OS=Web",
            "x-requested-with": "fetch",
            "x-zse-93": "101_3_3.0",
            "x-zse-96": "2.0_P8pmQV+P3QWo22U6D/fFbhCFlzFgB88o/LJyozaDnyXCDxxa+PrUus/NzDG0GcmS",
            "x-zst-81": "3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZs_Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIoLVqr4gxrRPOI0cY7HL8qun9g93mFukyigcmebS_FwOYPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTFHuYPvNMqCgqqgNM9BXfxBFKfBpmyw3GDq30WGoY8BL9kGo0EqgGHBxKXgSTVXC1FcCGDcLYUUgYy9gfZcpBNCOVTwoqY9OfcROq2ugBr_gGYDpmzwefk_LfuwFm0UeLeqNfbveMxwSBT9S_CbVfHCXLZwxC3ugKLUX19CF9SCg_6GV0Vg_zoqLfQLVKjvSL8GxBEDe8CbHBzgFmZcU0HgwpPUoMgrH_LbcGarOBQwoCEgC_AwXO_qCOhgYK3wNCUceCbHSs8gHYnG2_UgVYoipK1UVLs4xLQ7NCorxs",
        },
        cookies={},
    )

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
