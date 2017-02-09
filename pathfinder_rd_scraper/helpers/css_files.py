import ntpath
from typing import List, NamedTuple

import scrapy
from scrapy.http.response.html import HtmlResponse

CssFile = NamedTuple("CssFile", [("name", str), ("path", str), ("content", bytes)])


class CssExtractor:
    """Extract all css files from main page of Pathfinder Reference Document."""
    EXPECTED_FILENAME_PREFIX = "http://cdn.paizo.com/chrome/"

    def __init__(self, response: HtmlResponse) -> None:
        """Initialize instance."""
        self.main_page_response = response.copy()  # type: HtmlResponse
        self.files = []  # type: List[CssFile]

    def retrieve_css_files(self):
        """Retrieve all css files encountered."""
        pass

    def _get_css_files_addresses(self) -> List[str]:
        """Return list of all links to css files in document."""
        return self.main_page_response.xpath("//link[@rel='stylesheet']/@href").extract()

    def _load_css_files(self) -> List[CssFile]:
        """Load all css files found."""
        for css_uri in self._get_css_files_addresses():
            css_address_no_prefix = css_uri.replace(self.EXPECTED_FILENAME_PREFIX, "")
            file_name = ntpath.basename(css_address_no_prefix)
            path = css_address_no_prefix.replace(file_name, "")
            content = self._load_css_files()

    def _load_css_file(self) -> bytes:
        """Liad single css file content"""
        pass