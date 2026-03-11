from functools import partial
from pathlib import Path
from typing import TypeAlias

from .providers import (
    BaiduSerp,
    BilibiliSerp,
    BingSerp,
    BraveSerp,
    DouyinSerp,
    DuckDuckGoSerp,
    EngineConfig,
    GoogleSerp,
    RedditSerp,
    SerpItem,
    SoSerp,
    SogouSerp,
    ThreadsSerp,
    TiktokSerp,
    ToutiaoSerp,
    WeiboSerp,
    YandexSerp,
    YouTubeSerp,
    ZhihuSerp,
)
from .providers._base import load_engine_configs

ProviderName: TypeAlias = str

PROVIDERS = {
    "baidu": BaiduSerp,
    "bilibili": BilibiliSerp,
    "bing": BingSerp,
    "brave": BraveSerp,
    "douyin": DouyinSerp,
    "duckduckgo": DuckDuckGoSerp,
    "google": GoogleSerp,
    "reddit": RedditSerp,
    "so": SoSerp,
    "sogou": SogouSerp,
    "threads": ThreadsSerp,
    "tiktok": TiktokSerp,
    "toutiao": ToutiaoSerp,
    "weibo": WeiboSerp,
    "yandex": YandexSerp,
    "youtube": YouTubeSerp,
    "zhihu": ZhihuSerp,
}

SUPPORTED_ENGINES: tuple[EngineConfig, ...] = load_engine_configs()


def get_provider(name: ProviderName):
    return PROVIDERS[name]()


def parse_har(provider: str, har_path: str | Path) -> list[SerpItem]:
    return get_provider(provider).parse_har_file(har_path)


def search(keyword: str, provider: str = "google") -> list[SerpItem]:
    return get_provider(provider).query(keyword)


baidu = partial(search, provider="baidu")
bing = partial(search, provider="bing")
google = partial(search, provider="google")
