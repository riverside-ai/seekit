# pyserp

`pyserp` is a collection of APIs for search engine response page(SERP). Please be noted
that this is for research purpose only, especially for LLM, do not use it in production.

Currently, we have support for the following search engines:

- Google
- Bing
- DuckDuckGo
- Baidu
- Qihoo360
- Yandex
- X/Twitter
- Weibo

## Install

```
pip install pyserp --upgrade
```

## Usage

```py
import pyserp

results = pyserp.search("Taipei")
for result in results:
    print(result.title)
```
