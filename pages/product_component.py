"""Um produto compartilhado entre catálogo, carrinho e resumo."""

from decimal import ROUND_HALF_UP, Decimal

from playwright.sync_api import Page


def money(text: str) -> Decimal:
    # O site pode exibir resíduos de ponto flutuante no subtotal.
    # A comparação monetária é feita em centavos; diferenças de centavos falham.
    return Decimal(text.rsplit("$", 1)[-1].strip()).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


class ProductComponent:
    def __init__(self, page: Page, name: str):
        self.root = page.get_by_test_id("inventory-item").filter(
            has=page.get_by_text(name, exact=True)
        )
        self.name = self.root.get_by_test_id("inventory-item-name")
        self.price = self.root.get_by_test_id("inventory-item-price")
        self.quantity = self.root.get_by_test_id("item-quantity")
        self.add_button = self.root.get_by_role(
            "button", name="Add to cart", exact=True
        )
        self.remove_button = self.root.get_by_role("button", name="Remove", exact=True)

    def price_value(self):
        return money(self.price.inner_text())
