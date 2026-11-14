"""Operações no carrinho, independentes do checkout."""

import pytest
from playwright.sync_api import expect

from data.products import PRODUCTS

pytestmark = pytest.mark.cart


def test_remover_produto(inventory):
    inventory.add_products(PRODUCTS[:2])
    cart = inventory.open_cart().remove(PRODUCTS[0])
    expect(cart.items).to_have_count(1)
    expect(cart.names).to_have_text([PRODUCTS[1]])
    expect(cart.cart_badge).to_have_text("1")


def test_continuar_comprando_preserva_itens(inventory):
    inventory.add_products(PRODUCTS[:1])
    catalogue = inventory.open_cart().continue_shopping()
    expect(catalogue.title).to_have_text("Products")
    expect(catalogue.product(PRODUCTS[0]).remove_button).to_be_visible()
    expect(catalogue.cart_badge).to_have_text("1")
