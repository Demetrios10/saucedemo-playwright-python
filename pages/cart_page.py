"""Carrinho e navegação para checkout."""

from pages.base_page import BasePage
from pages.product_component import ProductComponent


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")

    def product(self, name):
        return ProductComponent(self.page, name)

    def remove(self, name):
        self.product(name).remove_button.click()
        return self

    def checkout(self):
        from pages.checkout_page import CheckoutInformationPage

        self.page.get_by_test_id("checkout").click()
        return CheckoutInformationPage(self.page)

    def continue_shopping(self):
        from pages.inventory_page import InventoryPage

        self.page.get_by_test_id("continue-shopping").click()
        return InventoryPage(self.page)
