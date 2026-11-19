"""Regressões para leitura de valores monetários do SauceDemo."""

from decimal import Decimal, InvalidOperation

import pytest

from pages.product_component import money


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("$29.99", Decimal("29.99")),
        ("Item total: $105.96000000000001", Decimal("105.96")),
        ("Tax: $8.48", Decimal("8.48")),
        ("Total: $114.44", Decimal("114.44")),
        ("$1.005", Decimal("1.01")),
        ("$1.004", Decimal("1.00")),
    ],
)
def test_money_normaliza_centavos(raw, expected):
    assert money(raw) == expected


@pytest.mark.parametrize("raw", ["$invalid", "$", "Total: $NaN?"])
def test_money_rejeita_valores_invalidos(raw):
    with pytest.raises(InvalidOperation):
        money(raw)


def test_money_nao_oculta_diferenca_de_um_centavo():
    assert money("$105.96") != money("$105.97")
