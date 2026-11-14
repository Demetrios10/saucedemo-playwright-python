# Arquitetura POM

Fluxo: LoginPage → InventoryPage → CartPage → CheckoutInformationPage → CheckoutOverviewPage → CheckoutCompletePage.

Páginas concentram seletores e ações. ProductComponent representa o produto no catálogo, carrinho e resumo. Testes mantêm asserções e comparação de valores. Fixtures configuram data-test e sessão independente por cenário. O hook de evidências registra setup, execução e teardown, sem armazenar credenciais.

