"""Catálogo de produtos."""

from pages.base_page import BasePage
from pages.product_component import ProductComponent


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")

    def product(self, name):
        return ProductComponent(self.page, name)

    def add_products(self, names):
        for name in names:
            self.product(name).add_button.click()
        return self
