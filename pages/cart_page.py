"""Carrinho e navegação para checkout."""

from pages.base_page import ProductListPage


class CartPage(ProductListPage):
    def remove(self, name: str) -> "CartPage":
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
