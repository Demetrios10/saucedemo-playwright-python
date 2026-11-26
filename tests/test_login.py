"""Login positivo e negativo, com sessão isolada por cenário."""

import re

import pytest
from playwright.sync_api import expect

from settings import settings

pytestmark = pytest.mark.login

INVENTORY_URL = re.compile(r"/inventory\.html$")
CATALOGUE_SIZE = 6


@pytest.mark.parametrize("use_enter", [False, True], ids=["botao", "enter"])
def test_login_valido(login_page, use_enter):
    inventory = login_page.login(settings.username, settings.password, use_enter)
    expect(inventory.title).to_have_text("Products")
    expect(inventory.page).to_have_url(INVENTORY_URL)
    expect(inventory.items).to_have_count(CATALOGUE_SIZE)


@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        ("", "", "Username is required"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("standard_user", "senha_incorreta", "Username and password do not match"),
        ("usuario_inexistente", "secret_sauce", "Username and password do not match"),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
    ],
    ids=[
        "campos-vazios",
        "sem-usuario",
        "sem-senha",
        "senha-incorreta",
        "usuario-inexistente",
        "usuario-bloqueado",
    ],
)
def test_login_negativo(login_page, username, password, message):
    login_page.login(username, password)
    expect(login_page.error).to_contain_text(message)
    expect(login_page.username_input).to_be_visible()
    expect(login_page.page).not_to_have_url(INVENTORY_URL)


def test_logout(inventory):
    login = inventory.logout()
    expect(login.login_button).to_be_visible()
    expect(login.username_input).to_have_value("")
