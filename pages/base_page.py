"""Navegação e elementos comuns; asserções de negócio ficam nos testes."""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.error = page.get_by_test_id("error")

    def open_cart(self):
        from pages.cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page)

    def logout(self):
        from pages.login_page import LoginPage

        self.page.get_by_role("button", name="Open Menu", exact=True).click()
        self.page.get_by_test_id("logout-sidebar-link").click()
        return LoginPage(self.page)
