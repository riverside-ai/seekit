from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text


class TiktokSerp(BaseSERP):
    provider = "tiktok"
    request_template = build_request_template(
        method="GET",
        url="https://www.tiktok.com/api/search/general/full/?WebIdLastTime=1773208761&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F145.0.0.0%20Safari%2F537.36&channel=tiktok_web&client_ab_versions=70508271%2C73720540%2C75136853%2C75182840%2C75204947%2C75260674%2C75294820%2C75331216%2C75350407%2C75381134%2C75381397%2C75413556%2C75436984%2C75440144%2C75492092%2C75528340%2C75602454%2C75602931%2C75611598%2C75613601%2C75637792%2C75654771%2C75665226%2C75667003%2C70405643%2C71057832%2C71200802%2C73004916%2C73171280%2C73208420%2C74008524%2C74276218%2C74413136%2C74844724%2C75330961&cookie_enabled=true&count=12&cursor=0&data_collection_enabled=false&device_id=7615873613828310529&device_platform=web_pc&device_type=web_h265&focus_state=true&from_page=search&history_len=3&is_fullscreen=false&is_non_personalized_search=0&is_page_visible=true&keyword=OpenClaw&odinId=7615873505791542279&offset=0&os=mac&priority_region=&referer=&region=JP&root_referer=https%3A%2F%2Fwww.tiktok.com%2F&screen_height=1107&screen_width=1710&search_source=normal_search&tz_name=Asia%2FShanghai&user_is_login=false&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_x%22%3A%7B%22search_engine%22%3A%7B%22ies_mt_user_live_video_card_use_libra%22%3A1%2C%22mt_search_general_user_live_card%22%3A1%7D%7D%2C%22search_server%22%3A%7B%7D%7D%7D&webcast_language=en&msToken=axd8fw2Y3p4wZVrogsIEzPhgvUorzffmP25C0gqxPYCOQouwqwnQCe8b-aAsOamF8gFyLXwarwg0fDE4NrpGAsCLEt3yxg9Na0wHFxVrMksmx13kVNznw8izqTQQ8k7w5pUlba4TKN8DN6Ha9-aVDT8=&X-Bogus=DFSzsIVOJFtANaUWCE1XThhGbwnD&X-Gnarly=M5AOOkOv-LtHVbPV/gavDA631XRxW-6GQDajsKsA6pYDQva2r7XUXxWmhTofT7DWQTKfeV7-pzV1Qg44b4L7de/oWcgNxM4d-nnBawRHqBkDNvexYLr6w7JnMUVsSA31uhyGeNK3fhgn5pORzrEBfwpqhwlzwMGexSNDfZY-xEuI7rn3H5T-veQyW4ulky7HMnxqz4yVf-hIJs6pHiB4nT2OD-6TJSJhfZ1wWWzFPt4P1Hj4yy0ntfoIc1fedR2XPzuTg-OEG1vkK9HRrphxwN9Ntrf3nvN9XlGynVL-VaeQ1hhLvgkdAzPmFwLuU0xrxcW=",
        headers={
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.tiktok.com/search?q=OpenClaw&t=1773208770199",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        },
        cookies={},
    )

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
