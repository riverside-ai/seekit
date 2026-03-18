from functools import partial
from dataclasses import dataclass
from typing import TypeAlias

from .providers import (
    BilibiliSerp,
    BingSerp,
    BraveSerp,
    DuckDuckGoSerp,
    RedditSerp,
    SerpItem,
    SoSerp,
    SogouSerp,
    ThreadsSerp,
    ToutiaoSerp,
    WeiboSerp,
    YouTubeSerp,
)

ProviderName: TypeAlias = str


@dataclass(frozen=True)
class EngineConfig:
    name: str
    type: str | None = None

PROVIDERS = {
    "bilibili": BilibiliSerp,
    "bing": BingSerp,
    "brave": BraveSerp,
    "duckduckgo": DuckDuckGoSerp,
    "reddit": RedditSerp,
    "so": SoSerp,
    "sogou": SogouSerp,
    "threads": ThreadsSerp,
    "toutiao": ToutiaoSerp,
    "weibo": WeiboSerp,
    "youtube": YouTubeSerp,
}

SUPPORTED_ENGINES: tuple[EngineConfig, ...] = (
    EngineConfig(name="bilibili", type="video"),
    EngineConfig(name="bing", type=None),
    EngineConfig(name="brave", type="web"),
    EngineConfig(name="duckduckgo", type="web"),
    EngineConfig(name="reddit", type="social"),
    EngineConfig(name="so", type="web"),
    EngineConfig(name="sogou", type="web"),
    EngineConfig(name="threads", type="social"),
    EngineConfig(name="toutiao", type="web"),
    EngineConfig(name="weibo", type="social"),
    EngineConfig(name="youtube", type="video"),
)


def get_provider(name: ProviderName):
    return PROVIDERS[name]()


def search(keyword: str, provider: str = "bing") -> list[SerpItem]:
    return get_provider(provider).query(keyword)


bing = partial(search, provider="bing")
