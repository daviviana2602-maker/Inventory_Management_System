# 📦 Inventory_Management_System

Sistema de **gestão de estoque via terminal** desenvolvido em **Python**, utilizando **SQLAlchemy (ORM)** e **PostgreSQL**.

O projeto foi criado como **estudo prático** para aplicar conceitos reais de backend, incluindo **CRUD completo, manipulação de banco de dados, validação de entradas e controle de fluxo de estoque**.

Além disso, o sistema foi pensado para simular o controle de estoque de uma **loja de roupas**, permitindo registrar produtos, vendas, retiradas e gerar resultados financeiros por período.

---

# 🚀 Objetivo do Projeto

Criar um sistema funcional que simule o fluxo real de um estoque, permitindo:

- cadastrar produtos
- atualizar quantidades automaticamente
- registrar vendas
- registrar retirada de produtos com motivo
- calcular lucros ou prejuízos automaticamente
- gerar relatórios financeiros por período
- visualizar dados diretamente do banco
- garantir que toda operação seja validada antes de entrar no banco de dados

---

# 📦 Tecnologias Utilizadas

- Python 3
- SQLAlchemy (ORM)
- PostgreSQL
- psycopg2
- Colorama
- Tabulate
- Datetime
- Módulo próprio (`fanymodules`)

---

# 🗄 Estrutura do Banco de Dados

O sistema utiliza **3 tabelas principais**.

---

## 1️⃣ estoque

Armazena todos os produtos disponíveis no estoque.

Campos:

- id
- product
- product_type
- size
- quantity
- purchase_price
- sale_price
- profit_reais
- profit_percent
- date

---

## 2️⃣ vendas

Registra todas as vendas realizadas.

Campos:

- id
- product
- product_type
- size
- quantity
- sale_unit_price
- sale_total_price
- sale_profit
- profitsale_percent
- date

---

## 3️⃣ retirados

Armazena produtos removidos do estoque e prejuízos.

Campos:

- id
- product
- product_type
- size
- unit_prejudice
- total_prejudice
- quantity
- reason
- date

---

# 🔥 Funcionalidades do Sistema

### ✔ Cadastro de produtos
- validação de nome, tipo, quantidade e preços
- cálculo automático de lucro
- atualização automática caso o produto já exista no estoque

---

### ✔ Registro de vendas
O sistema:

- verifica se o produto existe no estoque
- verifica se há quantidade suficiente
- calcula automaticamente lucro ou prejuízo
- atualiza o estoque
- remove o produto se a quantidade chegar a zero
- registra a venda na tabela **vendas**

---

### ✔ Retirada de produtos

Permite remover itens do estoque por motivos como:

- perda
- defeito
- erro de inventário

O sistema:

- calcula automaticamente o prejuízo
- registra o motivo da retirada
- atualiza o estoque
- remove o item caso a quantidade chegue a zero
- registra tudo na tabela **retirados**

---

### ✔ Consulta rápida de estoque

Permite verificar se um produto existe e qual sua quantidade atual.

---

### ✔ Alertas de estoque baixo

O sistema alerta automaticamente quando um produto possui **menos de 5 unidades**.

---

### ✔ Resultados financeiros por período

O usuário pode informar uma **data inicial e final**, e o sistema calcula:

- total vendido
- prejuízo com produtos retirados
- lucro total no período

---

### ✔ Visualização de tabelas

Permite visualizar diretamente no terminal as tabelas do banco:

- estoque
- vendas
- retirados

Os dados são exibidos em formato de tabela utilizando **Tabulate**.

---

# 🔁 Fluxo do Programa

1. O usuário escolhe uma operação no menu.
2. O sistema valida todos os inputs.
3. Os dados são manipulados no banco usando **SQLAlchemy**.
4. A operação correspondente é executada.
5. O sistema exibe mensagens claras e coloridas no terminal.
6. O usuário pode repetir a operação ou retornar ao menu.

---

# 📂 Organização do Código

O projeto possui aproximadamente **700 linhas de código**, organizadas em:

- menu principal
- definição das tabelas (ORM)
- funções separadas por operação
- lógica de validação de dados
- manipulação de banco via sessões
- loop principal do programa
- módulo externo (`fanymodules`) com funções auxiliares
