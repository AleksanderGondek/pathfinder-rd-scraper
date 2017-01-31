from typing import List

import scrapy

from pathfinder_rd_scraper.helpers.navigation import MainMenuExtractor, MenuEntry


class PathfinderRdSpider(scrapy.Spider):
    """To be described."""

    name = "PathfinderRd"
    initial_url = ""
    main_menu_urls = []  # type: List[MenuEntry]

    def _load_main_menu_urls(self) -> None:
        """To be described."""
        scrapy.Request(url=self.initial_url, callback=self._parse_maine_menu_for_urls)

    def _parse_maine_menu_for_urls(self, request: scrapy.Request) -> None:
        """To be described."""
        self.main_menu_urls.extend(MainMenuExtractor(request=request).retrieve_menu_links())

    def start_requests(self):
        """To be described."""
        self._load_main_menu_urls()
        for url in self.main_menu_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)