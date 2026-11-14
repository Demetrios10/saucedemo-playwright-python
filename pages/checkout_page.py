"""Informações, resumo e confirmação do pedido de demonstração."""

from pages.base_page import BasePage
from pages.product_component import ProductComponent, money


class CheckoutInformationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")

    def continue_with(self, first_name="", last_name="", postal_code=""):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.page.get_by_test_id("continue").click()
        return CheckoutOverviewPage(self.page)

    def cancel(self):
        from pages.cart_page import CartPage

        self.page.get_by_test_id("cancel").click()
        return CartPage(self.page)


class CheckoutOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")

    def product(self, name):
        return ProductComponent(self.page, name)

    def amounts(self):
        return tuple(
            money(field.inner_text()) for field in (self.subtotal, self.tax, self.total)
        )

    def finish(self):
        self.page.get_by_test_id("finish").click()
        return CheckoutCompletePage(self.page)


class CheckoutCompletePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.heading = page.get_by_test_id("complete-header")
        self.message = page.get_by_test_id("complete-text")

    def back_home(self):
        from pages.inventory_page import InventoryPage

        self.page.get_by_test_id("back-to-products").click()
        return InventoryPage(self.page)
