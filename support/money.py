"""Leitura de valores monetários exibidos pelo SauceDemo."""

from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")
CURRENCY_SYMBOL = "$"


def money(text: str) -> Decimal:
    """Converte textos como ``"Total: $114.44"`` em ``Decimal`` com centavos.

    O site pode exibir resíduos de ponto flutuante no subtotal, por isso o
    valor é arredondado para centavos; diferenças reais de centavos falham.
    """
    amount = text.rsplit(CURRENCY_SYMBOL, 1)[-1].strip()
    return Decimal(amount).quantize(CENTS, rounding=ROUND_HALF_UP)
