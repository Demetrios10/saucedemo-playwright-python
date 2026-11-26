"""Um produto compartilhado entre catálogo, carrinho e resumo."""

from decimal import Decimal

from playwright.sync_api import Page

from support.money import money

__all__ = ["ProductComponent", "money"]


class ProductComponent:
    def __init__(self, page: Page, name: str) -> None:
        self.root = page.get_by_test_id("inventory-item").filter(
            has=page.get_by_text(name, exact=True)
        )
        self.name = self.root.get_by_test_id("inventory-item-name")
        self.price = self.root.get_by_test_id("inventory-item-price")
        self.quantity = self.root.get_by_test_id("item-quantity")
        self.add_button = self.root.get_by_role("button", name="Add to cart", exact=True)
        self.remove_button = self.root.get_by_role("button", name="Remove", exact=True)

    def price_value(self) -> Decimal:
        return money(self.price.inner_text())
