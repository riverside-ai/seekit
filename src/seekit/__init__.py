from functools import partial
from dataclasses import dataclass
from typing import TypeAlias

from .providers import (
    BaiduSerp,
    BilibiliSerp,
    BingSerp,
    BraveSerp,
    DouyinSerp,
    DuckDuckGoSerp,
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

ProviderName: TypeAlias = str


@dataclass(frozen=True)
class EngineConfig:
    name: str
    type: str | None = None

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

SUPPORTED_ENGINES: tuple[EngineConfig, ...] = (
    EngineConfig(name="baidu", type="web"),
    EngineConfig(name="bilibili", type="video"),
    EngineConfig(name="bing", type=None),
    EngineConfig(name="brave", type="web"),
    EngineConfig(name="douyin", type="video"),
    EngineConfig(name="duckduckgo", type="web"),
    EngineConfig(name="google", type="web"),
    EngineConfig(name="reddit", type="social"),
    EngineConfig(name="so", type="web"),
    EngineConfig(name="sogou", type="web"),
    EngineConfig(name="threads", type="social"),
    EngineConfig(name="tiktok", type="video"),
    EngineConfig(name="toutiao", type="web"),
    EngineConfig(name="weibo", type="social"),
    EngineConfig(name="youtube", type="video"),
    EngineConfig(name="yandex", type="web"),
    EngineConfig(name="zhihu", type="social"),
)


def get_provider(name: ProviderName):
    return PROVIDERS[name]()


def search(keyword: str, provider: str = "google") -> list[SerpItem]:
    return get_provider(provider).query(keyword)


baidu = partial(search, provider="baidu")
bing = partial(search, provider="bing")
google = partial(search, provider="google")
