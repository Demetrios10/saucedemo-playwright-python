# Observação do site externo

Na primeira execução de 14/11/2026, o subtotal de quatro produtos foi exibido como `105.96000000000001`, enquanto a soma decimal dos preços foi `105.96`. A primeira rodada teve 19 aprovações e uma falha por essa diferença.

O helper money normaliza a leitura para duas casas com Decimal e ROUND_HALF_UP, pois as comparações do fluxo são monetárias. Diferenças de um centavo continuam reprovando o teste. Isso não corrige nem valida a formatação da interface do site: a anomalia visual permanece documentada aqui.
