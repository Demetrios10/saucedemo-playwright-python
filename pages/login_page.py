"""Página de login."""

from playwright.sync_api import Page

from pages.base_page import BasePage
from settings import settings


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")

    def open(self) -> "LoginPage":
        self.page.goto(settings.base_url, wait_until="domcontentloaded")
        return self

    def login(self, username: str, password: str, use_enter: bool = False):
        from pages.inventory_page import InventoryPage

        self.username_input.fill(username)
        self.password_input.fill(password)
        self._submit(use_enter)
        return InventoryPage(self.page)

    def _submit(self, use_enter: bool) -> None:
        if use_enter:
            self.password_input.press("Enter")
        else:
            self.login_button.click()
