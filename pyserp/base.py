from abc import abstractmethod
from typing import Optional

import lxml.html
import lxml_html_clean
from pydantic import BaseModel


class SerpItem(BaseModel):
    title: Optional[str]
    description: Optional[str]
    link: Optional[str]


class BaseSERP:
    CONTENT_XPATH = './/li[@class="res-list"]'
    AD_XPATH = './/span[text()="广告"]'

    def __init__(self):
        self.cleaner = lxml_html_clean.Cleaner(
            scripts=True,
            javascript=True,
            comments=True,
            style=True,
            links=False,
            meta=False,
            page_structure=False,
            processing_instructions=False,
            embedded=False,
            frames=False,
            forms=False,
            annoying_tags=True,
            remove_unknown_tags=False,
            safe_attrs_only=False,
        )

    @abstractmethod
    def get_trending(self):
        """Get trending topics from this Search engine"""

    @abstractmethod
    def request(self, keyword: str) -> str: ...

    @abstractmethod
    def _clean(self, tree) -> None: ...

    def clean(self, input_html):
        cleaned_html = self.cleaner.clean_html(input_html)

        tree = lxml.html.fromstring(cleaned_html)

        # Remove all <script> and <style> elements
        for element in tree.xpath("//script | //style"):
            element.getparent().remove(element)

        # Run customized clean hook
        self._clean(tree)

        return tree

    def extract(self, tree):
        items = tree.xpath(self.CONTENT_XPATH)

        clean_items = []
        for item in items:
            if not item.xpath(self.AD_XPATH):
                clean_items.append(item)
        return clean_items

    def query(self, keyword) -> list[SerpItem]:
        html = self.request(keyword)
        tree = self.clean(html)
        items = self.extract(tree)
        return items

    def test_file(self, filepath: str):
        with open(filepath) as f:
            items = self.extract(f.read())
        for item in items:
            print(lxml.html.tostring(item))
            print(item.text_content())

    def test_query(self, keyword: str):
        items = self.query(keyword)
        for item in items:
            print(lxml.html.tostring(item, encoding="unicode"))
            print(item.text_content())
