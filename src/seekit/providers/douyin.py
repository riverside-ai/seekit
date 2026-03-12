import json

from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text


class DouyinSerp(BaseSERP):
    provider = "douyin"
    request_template = build_request_template(
        method="GET",
        url="https://www.douyin.com/aweme/v1/web/general/search/stream/?aid=6383&browser_language=en&browser_name=Chrome&browser_online=true&browser_platform=MacIntel&browser_version=145.0.0.0&channel=channel_pc_web&cookie_enabled=true&count=10&cpu_core_num=10&device_memory=8&device_platform=webapp&disable_rs=0&downlink=6.85&effective_type=4g&enable_history=1&engine_name=Blink&engine_version=145.0.0.0&from_group_id=&is_filter_search=0&keyword=OpenClaw&list_type=&need_filter_settings=1&offset=0&os_name=Mac+OS&os_version=10.15.7&pc_client_type=1&pc_libra_divert=Mac&pc_search_top_1_params=%7B%22enable_ai_search_top_1%22%3A1%7D&platform=PC&query_correct_type=1&round_trip_time=150&screen_height=1107&screen_width=1710&search_channel=aweme_general&search_source=normal_search&support_dash=1&support_h265=1&uifid=749b770aa6a177ba6fbed42b6fcf8269d6ef3c63265bceaf64e3282dcaa6c732120d5f68b8ff72515bad3fb32f96875ac6b8eaeac215e5c1472333def2df202e85fd52a6942f6923fd4a252e26daf646e1a833d16c538b25a8ed79c26688ef0358665584896269cd9ab9562d4f74e804eb6ce14ac02b0d1239adc90b692f43431e9f3f986da81c2212468b6323af7a008c1c71530d7df55a73fc1b2f0336045d&update_version_code=0&version_code=190600&version_name=19.6.0&webid=7615873345917945398&msToken=8q7LR6EWzzOyU8feN6ITUskbuWHBmmvbmtw5IpzXzhzyLl1nLV2GB7a11oYsX7kOYuR7zzw_-ibLmwQ7xH-et3en75wjuIVKgPrGIlX-hR04jy_Vv_8bk_5HpAaPz1ZkvME6qFItBByXqwM3qoyQd1RA-hAJKBqoypNVfxIy3D6VRV6vKc8U9g%3D%3D&a_bogus=xfURh7SwxdRROdFSucN7CXql%2FCLANPuySPiKWHOT7POzaqFGeWPdsOaTGoLisbH78WpskolHifTlYDdbY0UhZHnpwmpfuO7jKUICnyso%2FqwvYFtBDqy8SwvzFwMu0YGwlAVJilXAZUao1jCWiHdL%2FQ599%2F%2FC5bgZBrORklTaO9Tp1%2FS121ZwiZs2Hfno54n2MblcyE%3D%3D",
        headers={
            "referer": "https://www.douyin.com/jingxuan/search/OpenClaw?aid=375ca68d-c565-434a-93d6-0ddf4da911e5&enter_from=discover&from_force_login=1&source=normal_search",
            "uifid": "749b770aa6a177ba6fbed42b6fcf8269d6ef3c63265bceaf64e3282dcaa6c732120d5f68b8ff72515bad3fb32f96875ac6b8eaeac215e5c1472333def2df202e85fd52a6942f6923fd4a252e26daf646e1a833d16c538b25a8ed79c26688ef0358665584896269cd9ab9562d4f74e804eb6ce14ac02b0d1239adc90b692f43431e9f3f986da81c2212468b6323af7a008c1c71530d7df55a73fc1b2f0336045d",
        },
        cookies={},
    )

    def parse_response(self, body: str) -> list[SerpItem]:
        payload = extract_json_from_text(body)
        items: list[SerpItem] = []
        for card in payload.get("data", []):
            for sub_card in card.get("sub_card_list", []):
                display = sub_card.get("common_aladdin", {}).get("display")
                if not display:
                    continue
                content = json.loads(display)
                hotspot = content.get("hotspot_info") or {}
                item = self.make_item(
                    title=hotspot.get("sentence"),
                    excerpt=hotspot.get("desc"),
                    url=hotspot.get("schema"),
                    author=hotspot.get("header"),
                    cover_url=(hotspot.get("board_icon") or {}).get("light"),
                )
                if item is not None:
                    items.append(item)
        return items
