# Variáveis de Ambiente para Railway

## Backend (Flask)

### Obrigatórias
- `SECRET_KEY`: Chave secreta da aplicação Flask
- `JWT_SECRET_KEY`: Chave secreta para tokens JWT
- `DATABASE_URL`: URL do banco PostgreSQL (fornecida automaticamente pelo Railway)

### Opcionais
- `FLASK_ENV`: production (padrão para Railway)
- `PORT`: Porta da aplicação (Railway define automaticamente)

## Frontend (React)

### Para Build
- `VITE_API_URL`: URL da API do backend (ex: https://seu-app.railway.app/api)

## Exemplo de Configuração

### Railway Backend
```
SECRET_KEY=rm-papel-secret-key-production-2024
JWT_SECRET_KEY=jwt-secret-string-rm-papel-production
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Railway Frontend (ou Vercel/Netlify)
```
VITE_API_URL=https://rm-papel-backend.railway.app/api
```

## Comandos para Deploy

### Backend no Railway
1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Railway detecta automaticamente Python e instala dependências
4. Aplicação roda na porta definida pelo Railway

### Frontend no Vercel/Netlify
1. Conectar repositório GitHub
2. Configurar VITE_API_URL
3. Build automático: `npm run build`
4. Deploy da pasta `dist/`

