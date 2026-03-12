from ._base import BaseSERP, SerpItem, build_request_template, extract_json_from_text, take_text


class ThreadsSerp(BaseSERP):
    provider = "threads"
    request_template = build_request_template(
        method="POST",
        url="https://www.threads.com/graphql/query",
        headers={
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-length": "1851",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.threads.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.threads.com/search",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-full-version-list": "\"Not:A-Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"145.0.7632.160\", \"Chromium\";v=\"145.0.7632.160\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-ch-ua-platform-version": "\"15.5.0\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-asbd-id": "359341",
            "x-bloks-version-id": "1363ee4ad31aa321b811ce30b2aacd0f644c2fb57f440040b43e585a4befa092",
            "x-csrftoken": "sOoEIgSPkdcC96GAu4oUfK",
            "x-fb-friendly-name": "useBarcelonaAccountSearchGraphQLDataSourceQuery",
            "x-fb-lsd": "AdSfYgvcmYhmLemaIyMOxQfi0Vw",
            "x-ig-app-id": "238260118697367",
            "x-logged-out-threads-migrated-request": "true",
            "x-root-field-name": "xdt_api__v1__users__search_connection",
            "x-web-session-id": "xssg2w:wv23lx:i7kr17",
        },
        cookies={},
        body="av=0&__user=0&__a=1&__req=t&__hs=20523.HCSV2%3Abarcelona_logged_out_pkg.2.1...0&dpr=2&__ccg=UNKNOWN&__rev=1034886289&__s=xssg2w%3Awv23lx%3Ai7kr17&__hsi=7615890921514195510&__dyn=7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W0qa0FE2awgo9oO0n24oaEd82lwv89k2C1Fwc60D85m1mzXwae4UaEW0Loco5G0zK5o4q0HU1IEGdwtU2ewbS1LwTwKG0hq1Iwqo9Epxq261bhEeEkyU8UaUuxq328Dxd0LCwWxW7E7C1jy8661Uw7cwkE&__csr=gP2dlEZTjnRhQ9hfqjt8DnAVnTO5y9UWzamXilwmQU7-0ye00q2K2-3efDwCg1983SxW1gg2nw5DxO6vXVe2604gy1K18x6u0CUfk0-e22m4ES8F0QAhNg26UyKWgjS0FA15O05EUEo0b6_w9Za0z_jw4wwFeiagQm15wo43y0f280HC8yB2WwKFpOhiyoQz2LB20e7CyE8E6d0-wgr4jyolK5Mq1Defgd4kQk0_8QwUywJK0OE7fhULI81e2N1a2q8AwbFw9W3GewuU2awYwqomwCxuFa95xcOxt1Eoew0yNze12DBxqU7a0jS4o6G09NDr80Ee02ru6CdAAyox08513Dgvg04g-58V4g0nQm0oe0e5Aw1GWcAw3qFE30xei&__hsdp=g2kIIh0DMt4bOIu3yskIAz55aaX5QlwxgwwQT4J248QcxG69o5I3Su35ZoBox281r8pweu2e5U5O1pw9i5VEbCEcU760wA2S0jG1Xw&__hblp=0Dg1o412AKh0gppFkubyKbu7osUy4ojyrAG2u7E7O1voF0Ixq0je12xB0nEpzU5S0C8dUCFoW5U6WdCzqCwPyoaofpbxm582LUO0qC1HDw&__sjsp=g2kIITb0AJ8Pgt4etsHa1hqSy18Eg5y43QM1iU&__comet_req=122&lsd=AdSfYgvcmYhmLemaIyMOxQfi0Vw&jazoest=22564&__spin_r=1034886289&__spin_b=trunk&__spin_t=1773212785&__crn=comet.barcelonawebloggedout.BarcelonaSearchColumnRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=useBarcelonaAccountSearchGraphQLDataSourceQuery&server_timestamps=true&variables=%7B%22query%22%3A%22OpenClaw%5C%5C%22%2C%22first%22%3A10%2C%22should_fetch_ig_inactive_on_text_app%22%3Anull%2C%22should_fetch_friendship_status%22%3Afalse%2C%22should_fetch_fediverse_profiles%22%3Afalse%2C%22hide_unconnected_private%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsLoggedInrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsCrawlerrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasDisplayNamesrelayprovider%22%3Afalse%7D&doc_id=34971288492470563",
    )

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
