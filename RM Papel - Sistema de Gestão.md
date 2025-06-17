# RM Papel - Sistema de Gestão

Sistema completo de gestão para papelaria personalizada, desenvolvido com Flask (backend) e React (frontend).

## 🚀 Deploy Rápido

### Backend (Railway)
1. Faça fork deste repositório
2. Conecte no [Railway](https://railway.app)
3. Configure as variáveis de ambiente:
   - `SECRET_KEY`: sua-chave-secreta
   - `JWT_SECRET_KEY`: sua-chave-jwt
4. Deploy automático!

### Frontend (Vercel/Netlify)
1. Configure a variável `VITE_API_URL` com a URL do seu backend
2. Deploy automático da pasta `rm-papel-frontend`

## 📁 Estrutura do Projeto

```
├── rm-papel-backend/     # API Flask
│   ├── src/
│   │   ├── models/       # Modelos do banco
│   │   ├── routes/       # Rotas da API
│   │   └── main.py       # Aplicação principal
│   ├── requirements.txt
│   └── README.md
├── rm-papel-frontend/    # Interface React
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── pages/        # Páginas
│   │   └── contexts/     # Contextos (Auth)
│   └── package.json
└── README.md
```

## 🔧 Desenvolvimento Local

### Backend
```bash
cd rm-papel-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python src/main.py
```

### Frontend
```bash
cd rm-papel-frontend
npm install
npm run dev
```

## 📊 Funcionalidades

- ✅ Autenticação JWT
- ✅ Gestão de Materiais e Fornecedores
- ✅ Cadastro de Produtos Personalizados
- ✅ Controle de Estoque
- ✅ Registro de Produção
- ✅ Gestão de Vendas e Clientes
- ✅ Controle Financeiro
- ✅ Dashboard com Métricas
- ✅ Relatórios em PDF
- ✅ Design Responsivo

## 🛠️ Tecnologias

**Backend:**
- Flask + SQLAlchemy
- PostgreSQL / SQLite
- JWT Authentication
- CORS enabled

**Frontend:**
- React + Vite
- Tailwind CSS + shadcn/ui
- Recharts para gráficos
- Axios para API

## 📝 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

