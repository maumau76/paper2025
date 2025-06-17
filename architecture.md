# Arquitetura do Sistema RM Papel

## Tecnologias Escolhidas

### Backend
- **Framework:** Flask (Python)
- **Banco de Dados:** PostgreSQL (via Railway)
- **ORM:** SQLAlchemy
- **Autenticação:** JWT (JSON Web Tokens)
- **Deploy:** Railway

### Frontend
- **Framework:** React.js
- **Estilização:** Tailwind CSS
- **Componentes:** shadcn/ui
- **Ícones:** Lucide React
- **Gráficos:** Recharts
- **Deploy:** Vercel/Netlify (via GitHub)

## Modelagem do Banco de Dados

### Tabela: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: suppliers (fornecedores)
```sql
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: materials (insumos)
```sql
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50) NOT NULL, -- unidade, metro, grama, etc.
    purchase_price DECIMAL(10,2) NOT NULL,
    stock_quantity DECIMAL(10,3) NOT NULL DEFAULT 0,
    min_stock_alert DECIMAL(10,3) DEFAULT 0,
    supplier_id INTEGER REFERENCES suppliers(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: categories (categorias de produtos)
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: products (produtos personalizados)
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    profit_margin DECIMAL(5,2) NOT NULL DEFAULT 0, -- porcentagem
    final_price DECIMAL(10,2),
    image_url VARCHAR(500),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: product_materials (relação produtos-insumos)
```sql
CREATE TABLE product_materials (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    material_id INTEGER REFERENCES materials(id),
    quantity_needed DECIMAL(10,3) NOT NULL, -- quantidade do insumo por unidade do produto
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: stock_movements (movimentações de estoque)
```sql
CREATE TABLE stock_movements (
    id SERIAL PRIMARY KEY,
    material_id INTEGER REFERENCES materials(id),
    movement_type VARCHAR(20) NOT NULL, -- 'IN' (entrada), 'OUT' (saída)
    quantity DECIMAL(10,3) NOT NULL,
    unit_price DECIMAL(10,2),
    total_cost DECIMAL(10,2),
    description TEXT,
    reference_id INTEGER, -- ID de referência (produção, venda, etc.)
    reference_type VARCHAR(50), -- 'purchase', 'production', 'sale'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: productions (produções)
```sql
CREATE TABLE productions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity_produced INTEGER NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    production_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: customers (clientes)
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: sales (vendas)
```sql
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    sale_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL, -- 'dinheiro', 'pix', 'cartao'
    total_amount DECIMAL(10,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: sale_items (itens da venda)
```sql
CREATE TABLE sale_items (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: expenses (despesas)
```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## APIs do Backend

### Autenticação
- `POST /api/auth/login` - Login do usuário
- `POST /api/auth/register` - Registro de novo usuário
- `POST /api/auth/logout` - Logout do usuário
- `GET /api/auth/me` - Dados do usuário logado

### Fornecedores
- `GET /api/suppliers` - Listar fornecedores
- `POST /api/suppliers` - Criar fornecedor
- `PUT /api/suppliers/{id}` - Atualizar fornecedor
- `DELETE /api/suppliers/{id}` - Deletar fornecedor

### Materiais (Insumos)
- `GET /api/materials` - Listar materiais
- `POST /api/materials` - Criar material
- `PUT /api/materials/{id}` - Atualizar material
- `DELETE /api/materials/{id}` - Deletar material
- `GET /api/materials/low-stock` - Materiais com estoque baixo

### Categorias
- `GET /api/categories` - Listar categorias
- `POST /api/categories` - Criar categoria
- `PUT /api/categories/{id}` - Atualizar categoria
- `DELETE /api/categories/{id}` - Deletar categoria

### Produtos
- `GET /api/products` - Listar produtos
- `POST /api/products` - Criar produto
- `PUT /api/products/{id}` - Atualizar produto
- `DELETE /api/products/{id}` - Deletar produto
- `POST /api/products/{id}/upload-image` - Upload de imagem do produto

### Movimentações de Estoque
- `GET /api/stock-movements` - Listar movimentações
- `POST /api/stock-movements` - Registrar movimentação

### Produções
- `GET /api/productions` - Listar produções
- `POST /api/productions` - Registrar produção
- `GET /api/productions/{id}` - Detalhes da produção

### Clientes
- `GET /api/customers` - Listar clientes
- `POST /api/customers` - Criar cliente
- `PUT /api/customers/{id}` - Atualizar cliente
- `DELETE /api/customers/{id}` - Deletar cliente

### Vendas
- `GET /api/sales` - Listar vendas
- `POST /api/sales` - Registrar venda
- `GET /api/sales/{id}` - Detalhes da venda
- `GET /api/sales/reports` - Relatórios de vendas

### Despesas
- `GET /api/expenses` - Listar despesas
- `POST /api/expenses` - Registrar despesa
- `PUT /api/expenses/{id}` - Atualizar despesa
- `DELETE /api/expenses/{id}` - Deletar despesa

### Dashboard
- `GET /api/dashboard/summary` - Resumo do dashboard
- `GET /api/dashboard/sales-chart` - Dados para gráfico de vendas
- `GET /api/dashboard/top-products` - Produtos mais vendidos

### Relatórios
- `GET /api/reports/financial` - Relatório financeiro
- `GET /api/reports/inventory` - Relatório de estoque
- `GET /api/reports/sales` - Relatório de vendas
- `GET /api/reports/export/pdf` - Exportar relatório em PDF

## Estrutura do Frontend

### Páginas Principais
1. **Login/Registro** (`/login`, `/register`)
2. **Dashboard** (`/`)
3. **Materiais** (`/materials`)
4. **Produtos** (`/products`)
5. **Estoque** (`/inventory`)
6. **Produção** (`/production`)
7. **Vendas** (`/sales`)
8. **Clientes** (`/customers`)
9. **Financeiro** (`/financial`)
10. **Relatórios** (`/reports`)
11. **Configurações** (`/settings`)

### Componentes Reutilizáveis
- **Layout Principal** - Sidebar, header, navegação
- **Tabelas de Dados** - Para listagem de itens
- **Formulários** - Para criação/edição
- **Modais** - Para confirmações e formulários rápidos
- **Gráficos** - Para dashboard e relatórios
- **Cards de Resumo** - Para métricas do dashboard
- **Upload de Imagem** - Para produtos
- **Filtros e Busca** - Para listagens

### Fluxos de Navegação
1. **Cadastro de Material** → Atualização automática do estoque
2. **Criação de Produto** → Seleção de materiais e cálculo de custo
3. **Registro de Produção** → Baixa automática de materiais do estoque
4. **Registro de Venda** → Baixa de produtos do estoque + entrada no financeiro
5. **Compra de Material** → Entrada no estoque + saída no financeiro

### Responsividade
- **Desktop:** Layout com sidebar fixa
- **Tablet:** Sidebar colapsável
- **Mobile:** Menu hambúrguer, layout em coluna única

## Configuração para Deploy

### GitHub
- Repositório único com backend e frontend em pastas separadas
- GitHub Actions para CI/CD automático
- Branches: `main` (produção), `develop` (desenvolvimento)

### Railway (Backend)
- Deploy automático via GitHub
- Variáveis de ambiente para configuração do banco
- PostgreSQL como addon

### Vercel/Netlify (Frontend)
- Deploy automático via GitHub
- Build do React otimizado para produção
- Configuração de variáveis de ambiente para API

