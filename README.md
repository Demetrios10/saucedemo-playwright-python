# SauceDemo — Python, Playwright e POM

Testes E2E do [SauceDemo](https://www.saucedemo.com/), ambiente demonstrativo sem cobrança financeira.

## Instalação no Windows

Na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium --only-shell
.\.venv\Scripts\python.exe -m pytest
```

Para assistir à execução:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest --headed
```

Não é preciso ativar o ambiente virtual. No Linux/macOS, use `.venv/bin/python`.

## Executar grupos

Use o Python do ambiente virtual:

```bash
python -m pytest -m login
python -m pytest -m checkout
python -m pytest -m cart
python -m pytest tests/test_checkout.py -k finalizar_compra
```

## Cenários

20 cenários independentes, incluindo parametrizações:

- Login correto pelo botão e Enter; logout.
- Campos vazios, usuário/senha ausentes, senha incorreta, usuário inexistente e usuário bloqueado.
- Compras finalizadas de **1, 2, 3, 4 e 5 produtos**.
- Validação de itens, quantidades, preços, subtotal, imposto exibido, total e confirmação.
- Nome, sobrenome e CEP obrigatórios.
- Cancelamento do checkout mantendo itens; remoção de produto; continuar comprando.

## Estrutura

```text
pages/       # Seletores e ações das páginas
data/        # Produtos e comprador fictício
tests/       # Cenários e asserções
support/     # Evidências automáticas
conftest.py  # Fixtures e isolamento
settings.py  # Configuração
docs/        # Arquitetura e plano de testes
evidencias/  # Resultado e capturas por cenário
```

Cada cenário usa um contexto novo. Não há pausas fixas nem tentativas automáticas para ocultar falhas. Valores monetários usam Decimal.

## Credenciais

Por padrão, usa a conta pública de demonstração fornecida na solicitação e exibida pelo site. Para substituir, defina `SAUCE_USERNAME` e `SAUCE_PASSWORD` no ambiente. `.env.example` é apenas referência; não é carregado automaticamente. Não use contas pessoais.

## Evidências

Cada execução gera `evidencias/execucoes/<UTC>/<cenario-hash>/resultado.json` e `tela-final.png`. As compras também capturam carrinho, resumo e confirmação. Campos de entrada são mascarados.

HTML e JUnit ficam em `artifacts/`. Não são gravados cookies, sessão ou traces com credenciais. Evidências geradas são ignoradas pelo Git; uma rodada revisada pode ser versionada separadamente.

## Limitações

O site é externo e pode mudar ou ficar indisponível. O subtotal é comparado aos preços do catálogo; o total ao subtotal mais o imposto exibido. Não se verificam pagamento real, entrega física ou backend de produção.

[Arquitetura](docs/ARQUITETURA.md) · [Plano de testes](docs/CENARIOS.md)

