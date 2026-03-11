# seekit

`seekit` wraps multiple search providers behind a common `SerpItem` model and can search
live using `curl_cffi` request templates derived from captured HAR files.

Supported providers:

- Baidu
- Bilibili
- Bing
- Brave
- Douyin
- DuckDuckGo
- Google
- Reddit
- So.com
- Sogou
- Threads
- TikTok
- Toutiao
- Weibo
- Yandex
- YouTube
- Zhihu

## Install

```bash
uv add seekit
```

For the CLI:

```bash
uv tool install seekit
```

## Usage

Search live:

```python
import seekit

results = seekit.search("latest OpenAI reasoning model", provider="google")
for item in results[:3]:
    print(item.provider, item.title, item.url)
```

CLI:

```bash
seekit tiktok OpenAI
seekit google latest OpenAI reasoning model --limit 5
```

Each parsed item uses the shared pydantic model:

```python
class SerpItem(BaseModel):
    provider: str
    title: str | None
    excerpt: str | None
    url: str | None
    author: str | None
    cover_url: str | None
```

Fixture parsing is still available for tests and parser debugging:

```python
from pathlib import Path

results = seekit.parse_har("google", Path("data/pages/google.har"))
```

## Development

```bash
uv run pytest
```

Tests read the HAR fixtures under [`data/pages`](./data/pages), verify the normalized item
shape, and validate that live request templates substitute the search keyword correctly.

## Release

```bash
make publish-testpypi
make publish-pypi
```

These targets build with `uv build` and publish with `uvx uv-publish`.
