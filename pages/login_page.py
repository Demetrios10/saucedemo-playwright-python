"""Página de login."""

from pages.base_page import BasePage
from settings import settings


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")

    def open(self):
        self.page.goto(settings.base_url, wait_until="domcontentloaded")
        return self

    def login(self, username, password, use_enter=False):
        from pages.inventory_page import InventoryPage

        self.username_input.fill(username)
        self.password_input.fill(password)
        if use_enter:
            self.password_input.press("Enter")
        else:
            self.login_button.click()
        return InventoryPage(self.page)
