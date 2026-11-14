# Execução — 14/11/2026

20 cenários aprovados em Chromium headless em 54,69 segundos.

Compras de 1, 2, 3, 4 e 5 produtos foram finalizadas até a confirmação, com conferência de itens, preços e totais.

A primeira rodada teve 19 aprovações e uma falha por resíduo de ponto flutuante no subtotal de quatro itens. A comparação passou a usar a precisão monetária de centavos; a anomalia visual está documentada em docs/ANOMALIAS.md.

Cada cenário tem seu resultado.json e captura final. As cinco compras têm capturas adicionais do carrinho, resumo e confirmação. São simulações no ambiente público SauceDemo, sem cobrança ou entrega real.

Black e Ruff verificaram formatação e importações.
