# Inventory_Management_System

Este é um sistema de gestão de estoque desenvolvido do zero, utilizando Python, SQLAlchemy (ORM) e PostgreSQL.
O projeto foi criado inteiramente como estudo prático para entender na prática CRUD, tabelas relacionais, validação de dados e manipulação real de estoque e vendas.



-------------------------------------------------------------------------------------------------
🚀 ## Objetivo do Projeto ##

Criar um sistema funcional que simula um fluxo completo de estoque:
- cadastrar produtos
- registrar compras
- registrar vendas
- retirar peças com motivo
- atualizar quantidades em tempo real
- calcular lucros/prejuízos por peça
- movimentar dados entre tabelas
- garantir que cada operação seja validada antes de entrar no banco
* Tudo isso usando conceitos essenciais de backend e banco de dados.



-------------------------------------------------------------------------------------------------
📦 #Tecnologias Utilizadas

- Python 3
- SQLAlchemy ORM
- PostgreSQL
- psycopg2
- Colorama
- Datetime
- Módulo próprio (fanymodules)



-------------------------------------------------------------------------------------------------
🧱 #Estrutura do Banco de Dados
O projeto utiliza 3 tabelas principais:

1. #estoque
- Armazena tudo sobre produtos disponíveis:
- nome
- tipo
- tamanho
- quantidade
- preço de compra
- preço de venda
- lucro por peça
- lucro em porcentagem
- data da compra

2. #vendas
- Registra toda venda feita:
- nome do produto
- tipo
- tamanho
- preço vendido
- lucro/prejuízo real por peça
- porcentagem de lucro/prejuízo
- quantidade vendida
- data da venda

3. #retirados
- Guarda retiradas e perdas do estoque:
- produto
- tipo
- tamanho
- quantidade retirada
- preço original
- motivo da retirada
- data



-------------------------------------------------------------------------------------------------
🔥 #Principais Funcionalidades

✔ Cadastro completo de produtos
- Com validações rígidas de nome, tipo, tamanho, quantidade e preços.

✔ Registro de venda 100% validado
- verifica se o item existe
- verifica se há estoque suficiente
- calcula lucro ou prejuízo real
- atualiza o estoque automaticamente
- remove item da tabela se quantidade chegar a zero
- salva venda na tabela correta

✔ Retirada de peças com motivo
- valida tudo
- mantém histórico completo de perdas
- atualiza estoque
- exclui o item se zerar

✔ Consulta rápida ao estoque
- Verificação direta e validada.

✔ Cálculo automático:
- lucro em reais
- lucro em porcentagem
- prejuízo por peça
- atualizações consistentes no banco
  
-------------------------------------------------------------------------------------------------

- ✔ Separação de responsabilidade entre tabelas
- ✔ Uso de ORM profissional (SQLAlchemy)
- ✔ Sessões com commit/rollback para segurança dos dados
- ✔ Entradas 100% tratadas e validadas



-------------------------------------------------------------------------------------------------
🧩 #Fluxo do Programa

- Usuário escolhe a operação no menu.
- O sistema valida todos os inputs.
- Busca e manipula dados no banco via SQLAlchemy.
- Executa o CRUD correspondente.
- Mostra mensagens claras e coloridas (Colorama).
- Permite repetir a operação ou voltar ao menu.



-------------------------------------------------------------------------------------------------
📂 #Organização do Código

*Aproximadamente 490 linhas
*Estruturado em:

- menu
- classes/tabelas
- funções separadas por operação
- loop principal
- módulo externo (fanymodules) para funções de repetição
- responsabilidade de tabelas
