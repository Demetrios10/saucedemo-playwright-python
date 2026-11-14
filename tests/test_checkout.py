"""Compras reais no ambiente demonstrativo, sem cobrança financeira."""

from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data.products import CUSTOMER, PRODUCTS

pytestmark = pytest.mark.checkout


@pytest.mark.parametrize("quantity", [1, 2, 3, 4, 5], ids=lambda n: f"{n}-produtos")
def test_finalizar_compra(inventory, quantity, evidence_step):
    selected = PRODUCTS[:quantity]
    prices = {name: inventory.product(name).price_value() for name in selected}
    inventory.add_products(selected)
    expect(inventory.cart_badge).to_have_text(str(quantity))

    cart = inventory.open_cart()
    expect(cart.items).to_have_count(quantity)
    expect(cart.names).to_have_text(list(selected))
    for name in selected:
        expect(cart.product(name).quantity).to_have_text("1")
        assert cart.product(name).price_value() == prices[name]
    evidence_step("01-carrinho")

    information = cart.checkout()
    overview = information.continue_with(**CUSTOMER)
    expect(overview.title).to_have_text("Checkout: Overview")
    expect(overview.items).to_have_count(quantity)
    expect(overview.names).to_have_text(list(selected))
    for name in selected:
        assert overview.product(name).price_value() == prices[name]
    subtotal, tax, total = overview.amounts()
    assert subtotal == sum(prices.values(), Decimal("0.00"))
    assert tax >= Decimal("0.00")
    assert total == subtotal + tax
    evidence_step("02-resumo")

    complete = overview.finish()
    expect(complete.heading).to_have_text("Thank you for your order!")
    expect(complete.message).to_contain_text("Your order has been dispatched")
    expect(complete.cart_badge).to_have_count(0)
    evidence_step("03-compra-finalizada")
    catalogue = complete.back_home()
    expect(catalogue.title).to_have_text("Products")
    expect(catalogue.cart_badge).to_have_count(0)


@pytest.mark.parametrize(
    "first_name,last_name,postal_code,error",
    [
        ("", "", "", "First Name is required"),
        ("Pessoa", "", "", "Last Name is required"),
        ("Pessoa", "Teste", "", "Postal Code is required"),
    ],
    ids=["sem-nome", "sem-sobrenome", "sem-cep"],
)
def test_checkout_campos_obrigatorios(
    inventory, first_name, last_name, postal_code, error
):
    inventory.add_products(PRODUCTS[:1])
    information = inventory.open_cart().checkout()
    information.continue_with(first_name, last_name, postal_code)
    expect(information.error).to_contain_text(error)
    expect(information.title).to_have_text("Checkout: Your Information")


def test_cancelar_checkout_preserva_carrinho(inventory):
    inventory.add_products(PRODUCTS[:2])
    cart = inventory.open_cart().checkout().cancel()
    expect(cart.title).to_have_text("Your Cart")
    expect(cart.names).to_have_text(list(PRODUCTS[:2]))
