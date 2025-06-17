# RM Papel - Sistema de Gestão para Papelaria

## Descrição
Sistema completo de gestão para papelaria personalizada, desenvolvido em Flask (Python) para controle de materiais, produtos, estoque, produção, vendas e financeiro.

## Funcionalidades

### 🔐 Autenticação
- Login e registro de usuários
- Autenticação JWT
- Proteção de rotas

### 📦 Gestão de Materiais
- Cadastro de fornecedores
- Cadastro de materiais/insumos
- Controle de estoque
- Alertas de estoque baixo
- Histórico de movimentações

### 🎨 Gestão de Produtos
- Cadastro de categorias
- Cadastro de produtos personalizados
- Cálculo automático de custos
- Definição de margem de lucro
- Upload de imagens

### 🏭 Controle de Produção
- Registro de produções
- Baixa automática de materiais
- Cálculo de custos por lote
- Atualização de estoque de produtos

### 💰 Gestão de Vendas
- Cadastro de clientes
- Registro de vendas
- Múltiplos métodos de pagamento
- Baixa automática de estoque
- Relatórios de vendas

### 📊 Financeiro
- Controle de despesas
- Fluxo de caixa
- Relatórios financeiros
- Dashboard com métricas

### 📈 Dashboard e Relatórios
- Resumo executivo
- Gráficos de vendas
- Produtos mais vendidos
- Exportação em PDF

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **ORM**: SQLAlchemy
- **Autenticação**: JWT
- **CORS**: Flask-CORS
- **Migrações**: Flask-Migrate
- **Relatórios PDF**: ReportLab

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip

### Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd rm-papel-backend
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (opcional):
```bash
export SECRET_KEY="sua-chave-secreta"
export JWT_SECRET_KEY="sua-chave-jwt"
export DATABASE_URL="postgresql://user:pass@host:port/dbname"  # Para PostgreSQL
```

5. Execute o servidor:
```bash
python src/main.py
```

O servidor estará disponível em `http://localhost:5000`

## Deploy no Railway

### 1. Preparação
- Certifique-se de que o `requirements.txt` está atualizado
- O arquivo `src/main.py` já está configurado para Railway

### 2. Deploy
1. Faça push do código para o GitHub
2. Conecte o repositório no Railway
3. Configure as variáveis de ambiente:
   - `SECRET_KEY`: Chave secreta da aplicação
   - `JWT_SECRET_KEY`: Chave secreta para JWT
   - `DATABASE_URL`: URL do PostgreSQL (Railway fornece automaticamente)

### 3. Banco de Dados
- Railway criará automaticamente um banco PostgreSQL
- As tabelas serão criadas automaticamente na primeira execução

## Estrutura da API

### Autenticação
- `POST /api/auth/register` - Registro de usuário
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Dados do usuário logado
- `POST /api/auth/logout` - Logout

### Fornecedores
- `GET /api/suppliers` - Listar fornecedores
- `POST /api/suppliers` - Criar fornecedor
- `PUT /api/suppliers/{id}` - Atualizar fornecedor
- `DELETE /api/suppliers/{id}` - Deletar fornecedor

### Materiais
- `GET /api/materials` - Listar materiais
- `POST /api/materials` - Criar material
- `PUT /api/materials/{id}` - Atualizar material
- `DELETE /api/materials/{id}` - Deletar material
- `GET /api/materials/low-stock` - Materiais com estoque baixo
- `POST /api/materials/{id}/add-stock` - Adicionar estoque

### Categorias
- `GET /api/categories` - Listar categorias
- `POST /api/categories` - Criar categoria
- `PUT /api/categories/{id}` - Atualizar categoria
- `DELETE /api/categories/{id}` - Deletar categoria

### Produtos
- `GET /api/products` - Listar produtos
- `POST /api/products` - Criar produto
- `GET /api/products/{id}` - Detalhes do produto
- `PUT /api/products/{id}` - Atualizar produto
- `DELETE /api/products/{id}` - Deletar produto
- `GET /api/products/{id}/calculate-price` - Calcular preço

### Movimentações de Estoque
- `GET /api/stock-movements` - Listar movimentações
- `POST /api/stock-movements` - Registrar movimentação

### Produções
- `GET /api/productions` - Listar produções
- `POST /api/productions` - Registrar produção
- `GET /api/productions/{id}` - Detalhes da produção
- `DELETE /api/productions/{id}` - Deletar produção

### Clientes
- `GET /api/customers` - Listar clientes
- `POST /api/customers` - Criar cliente
- `PUT /api/customers/{id}` - Atualizar cliente
- `DELETE /api/customers/{id}` - Deletar cliente

### Vendas
- `GET /api/sales` - Listar vendas
- `POST /api/sales` - Registrar venda
- `GET /api/sales/{id}` - Detalhes da venda
- `DELETE /api/sales/{id}` - Deletar venda
- `GET /api/sales/reports` - Relatórios de vendas

### Despesas
- `GET /api/expenses` - Listar despesas
- `POST /api/expenses` - Registrar despesa
- `PUT /api/expenses/{id}` - Atualizar despesa
- `DELETE /api/expenses/{id}` - Deletar despesa
- `GET /api/expenses/categories` - Categorias de despesas

### Dashboard
- `GET /api/dashboard/summary` - Resumo do dashboard
- `GET /api/dashboard/sales-chart` - Dados para gráfico de vendas
- `GET /api/dashboard/top-products` - Produtos mais vendidos

### Relatórios
- `GET /api/reports/financial` - Relatório financeiro
- `GET /api/reports/inventory` - Relatório de estoque
- `GET /api/reports/sales` - Relatório de vendas
- `GET /api/reports/export/pdf` - Exportar relatório em PDF

## Modelo de Dados

### Principais Entidades
- **Users**: Usuários do sistema
- **Suppliers**: Fornecedores
- **Materials**: Materiais/insumos
- **Categories**: Categorias de produtos
- **Products**: Produtos personalizados
- **ProductMaterials**: Relação produtos-materiais
- **StockMovements**: Movimentações de estoque
- **Productions**: Registros de produção
- **Customers**: Clientes
- **Sales**: Vendas
- **SaleItems**: Itens das vendas
- **Expenses**: Despesas

## Segurança

- Todas as rotas (exceto login/register) requerem autenticação JWT
- Senhas são criptografadas com bcrypt
- CORS configurado para permitir acesso do frontend
- Validação de dados de entrada

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Suporte

Para suporte, entre em contato através do email ou abra uma issue no GitHub.

