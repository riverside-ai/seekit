from functools import partial
from .qihoo import QihooSerp
from .baidu import BaiduSerp


def search(keyword, provider="google"):
    ...



baidu = partial(search, provider="baidu")
bing = partial(search, provider="bing")
google = partial(search, provider="google")
