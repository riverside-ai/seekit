from __future__ import annotations

from html import escape

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn

from . import PROVIDERS, search

app = FastAPI(title="seekit", version="0.0.1")


def render_page(provider: str, keyword: str, rows: list[dict[str, str | None]]) -> str:
    options = []
    for name in sorted(PROVIDERS):
        selected = " selected" if name == provider else ""
        options.append(f'<option value="{escape(name)}"{selected}>{escape(name)}</option>')
    parts = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><title>seekit</title>",
        "<style>body{font-family:ui-sans-serif,system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;background:#faf8f2;color:#1f2937}form{display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:1.5rem}input,select,button{padding:.65rem .8rem;border:1px solid #d1d5db;border-radius:.5rem;font:inherit}button{background:#111827;color:#fff;border-color:#111827}table{width:100%;border-collapse:collapse;background:#fff;border-radius:.75rem;overflow:hidden}th,td{padding:.75rem;border-bottom:1px solid #e5e7eb;text-align:left;vertical-align:top}th{background:#f3f4f6}small{color:#6b7280}</style>",
        "</head><body>",
        "<h1>seekit</h1>",
        "<form method='get' action='/'>",
        f"<select name='provider'>{''.join(options)}</select>",
        f"<input type='text' name='q' placeholder='Search keyword' value='{escape(keyword)}' style='flex:1;min-width:18rem'>",
        "<button type='submit'>Search</button>",
        "</form>",
    ]
    if rows:
        parts.append("<table><thead><tr><th>Provider</th><th>Title</th><th>Author</th><th>Time</th><th>URL</th></tr></thead><tbody>")
        for row in rows:
            url = row["url"] or ""
            link = f"<a href='{escape(url)}'>{escape(url)}</a>" if url else ""
            parts.append(
                "<tr>"
                f"<td>{escape(row['provider'] or '')}</td>"
                f"<td>{escape(row['title'] or '')}<br><small>{escape(row['excerpt'] or '')}</small></td>"
                f"<td>{escape(row['author'] or '')}</td>"
                f"<td>{escape(row['time'] or '')}</td>"
                f"<td>{link}</td>"
                "</tr>"
            )
        parts.append("</tbody></table>")
    parts.append("</body></html>")
    return "".join(parts)


@app.get("/api/search")
def api_search(
    q: str = Query(..., min_length=1),
    provider: str = Query("google"),
) -> list[dict[str, str | None]]:
    return [item.model_dump(mode="json") for item in search(q, provider=provider)]


@app.get("/", response_class=HTMLResponse)
def index(
    q: str = Query("", alias="q"),
    provider: str = Query("google"),
) -> HTMLResponse:
    rows: list[dict[str, str | None]] = []
    if q:
        rows = [item.model_dump(mode="json") for item in search(q, provider=provider)]
    return HTMLResponse(render_page(provider, q, rows))


def main() -> None:
    uvicorn.run("seekit.server:app", host="127.0.0.1", port=8000)
