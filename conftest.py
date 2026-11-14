"""Fixtures: contexto novo por cenário, sem sessão compartilhada."""

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from settings import settings

pytest_plugins = ("support.evidence", "support.steps")


@pytest.fixture(scope="session", autouse=True)
def configure_test_ids(playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 1000},
        "locale": "en-US",
    }


@pytest.fixture
def login_page(page):
    return LoginPage(page).open()


@pytest.fixture
def inventory(login_page):
    catalogue = login_page.login(settings.username, settings.password)
    expect(catalogue.title).to_have_text("Products")
    return catalogue
