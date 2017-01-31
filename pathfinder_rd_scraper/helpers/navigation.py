import parsel
from typing import List, NamedTuple

from scrapy.http.response.html import HtmlResponse

MenuEntry = NamedTuple("MenuEntry", [("group", str), ("name", str), ("link", str)])


class MainMenuExtractor:
    """Extract all links from main menu of Pathfinder Reference Document."""
    URL_GROUPS_SEPARATOR = "-"

    def __init__(self, response: HtmlResponse) -> None:
        """Initialize instance."""
        self.main_page_response = response.copy()  # type: HtmlResponse
        self.urls = []  # type: List[MenuEntry]

    def retrieve_menu_links(self) -> List[MenuEntry]:
        """Return list of entries from main menu."""
        if self.urls:
            return self.urls

        list_of_main_menu_items = self._get_list_of_items_from_main_menu()
        self._parse_list_of_menu_items(items=list_of_main_menu_items)
        return self.urls.copy()

    def _get_list_of_items_from_main_menu(self) -> parsel.SelectorList:
        """Return selector list containing main menu items."""
        main_menu_div = self.main_page_response.xpath("//div[@id='menu']")
        main_menu_list = main_menu_div.xpath("./ul")
        return main_menu_list.xpath("./li")

    def _parse_list_of_menu_items(self, items: parsel.SelectorList, parent_name: str="") -> None:
        """Parse items from main menu html into list of urls."""
        for item in items:
            if item.css(".has-subnav"):
                final_parent_name = self._get_final_parent_name_for_entry_with_nested_items(entry=item,
                                                                                            parent_name=parent_name)
                item_nested_elements = item.xpath("./ul")[0].xpath("./li")
                self._parse_list_of_menu_items(items=item_nested_elements, parent_name=final_parent_name)
            else:
                self._parse_menu_item_without_nested_items(item=item, parent_name=parent_name)

    def _parse_menu_item_without_nested_items(self, item: parsel.SelectorList,
                                              parent_name: str="") -> None:
        """Create single menu entry."""
        link_name = ""
        if item.xpath("./a/i/text()"):
            link_name = item.xpath("./a/i/text()").extract_first()
        link_name += str(item.xpath("./a/text()").extract_first())
        link_href = item.xpath("./a/@href").extract_first()

        self.urls.append(MenuEntry(parent_name, link_name, link_href))

    @classmethod
    def _get_final_parent_name_for_entry_with_nested_items(cls, entry: parsel.SelectorList,
                                                           parent_name=None) -> str:
        """
        Return final parent element to be used.

        Thanks to this method, menu items that are nested in multiple sections,
        will have group name as <section_one>-<section_two>..
        """
        entry_content = entry.xpath("./a/text()").extract_first()
        if not parent_name:
            return entry_content

        return parent_name + cls.URL_GROUPS_SEPARATOR + entry_content
