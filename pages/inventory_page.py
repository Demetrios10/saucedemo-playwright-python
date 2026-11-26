"""Catálogo de produtos."""

from collections.abc import Iterable

from pages.base_page import ProductListPage


class InventoryPage(ProductListPage):
    def add_products(self, names: Iterable[str]) -> "InventoryPage":
        for name in names:
            self.product(name).add_button.click()
        return self
