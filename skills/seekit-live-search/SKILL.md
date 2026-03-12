---
name: seekit-live-search
description: Use this skill when an agent needs fresh web results through seekit. It explains how to choose a provider, call seekit.search for live network fetches, and consume the normalized SerpItem fields for latest-information tasks.
---

# Seekit Live Search

Use this skill for live web search through `seekit`.

## Workflow

1. Pick the provider that best fits the request:
   - `google`, `bing`, `brave`, `duckduckgo`, `baidu`, `so`, `sogou`, `yandex`, `toutiao` for web
   - `youtube`, `bilibili`, `douyin`, `tiktok` for video
   - `reddit`, `threads`, `weibo`, `zhihu` for social
2. Call `seekit.search(query, provider=...)`.
3. Read the normalized fields on each `SerpItem`:
   - `provider`
   - `title`
   - `excerpt`
   - `url`
   - optional `author`
   - optional `cover_url`
4. If one provider looks thin or noisy, retry with a second provider instead of overfitting the parser output.

## Notes

- `seekit` uses HAR-derived request templates for live fetches.
- Use `seekit.parse_har(...)` only for parser debugging or fixture tests, not for fresh search results.
