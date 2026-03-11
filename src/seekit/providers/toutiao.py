import re

from ._base import BaseSERP, SerpItem


class ToutiaoSerp(BaseSERP):
    provider = "toutiao"

    def parse_response(self, body: str) -> list[SerpItem]:
        pattern = re.compile(
            r'"title":"(?P<title>[^"]+?)".{0,1200}?"abstract":"(?P<excerpt>[^"]+?)".{0,1200}?"open_url":"(?P<url>http[^"]+)".{0,1200}?"media_name":"(?P<author>[^"]*?)"',
            re.S,
        )
        items: list[SerpItem] = []
        for match in pattern.finditer(body):
            built = self.make_item(
                title=match.group("title"),
                excerpt=match.group("excerpt"),
                url=match.group("url"),
                author=match.group("author") or None,
            )
            if built is not None:
                items.append(built)
        return items
