---
name: seekit-latest-info
description: Use this skill when an agent needs latest information on a keyword and should use seekit as the first retrieval step. It covers provider selection, multi-provider fallback, and how to turn SerpItem results into sourced, up-to-date answers.
---

# Seekit Latest Info

Use this skill when the task is "find the latest info on X".

## Workflow

1. Start with one high-signal provider.
2. Run `seekit.search(keyword, provider=...)`.
3. Inspect `title`, `excerpt`, `url`, and optional `author`.
4. If freshness or coverage looks weak, run a second provider and compare.
5. Cite the destination URLs in the final answer.

## Provider Defaults

- General web: `google` or `bing`
- Social chatter: `reddit`, `threads`, `weibo`, `zhihu`
- Video/news clips: `youtube`, `bilibili`, `douyin`, `tiktok`

## Notes

- Prefer provider diversity over repeated queries against the same source.
- Keep the final answer grounded in the returned URLs, not just the snippets.
