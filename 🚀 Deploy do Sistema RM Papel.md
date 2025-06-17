# 🚀 Deploy do Sistema RM Papel

## Opção 1: Deploy Automático via GitHub + Railway

### 1. Subir para GitHub
```bash
# Criar repositório no GitHub (via interface web)
# Depois executar:
git remote add origin https://github.com/SEU_USUARIO/rm-papel-sistema.git
git branch -M main
git push -u origin main
```

### 2. Deploy do Backend no Railway
1. Acesse [Railway.app](https://railway.app)
2. Conecte sua conta GitHub
3. Clique em "New Project" → "Deploy from GitHub repo"
4. Selecione o repositório `rm-papel-sistema`
5. Railway detectará automaticamente o Python
6. Configure as variáveis de ambiente:
   - `SECRET_KEY`: rm-papel-secret-key-production-2024
   - `JWT_SECRET_KEY`: jwt-secret-string-rm-papel-production
7. Railway criará automaticamente um banco PostgreSQL
8. Deploy automático! 🎉

### 3. Deploy do Frontend no Vercel
1. Acesse [Vercel.com](https://vercel.com)
2. Conecte sua conta GitHub
3. Clique em "New Project"
4. Selecione o repositório `rm-papel-sistema`
5. Configure:
   - **Root Directory**: `rm-papel-frontend`
   - **Framework Preset**: Vite
   - **Environment Variables**: 
     - `VITE_API_URL`: https://SEU-APP.railway.app/api
6. Deploy automático! 🎉

## Opção 2: Deploy Manual

### Backend (Railway)
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd rm-papel-backend
railway deploy
```

### Frontend (Vercel)
```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy
cd rm-papel-frontend
vercel --prod
```

## 📋 Checklist de Deploy

### Backend
- [ ] Repositório no GitHub criado
- [ ] Railway conectado ao GitHub
- [ ] Variáveis de ambiente configuradas
- [ ] Banco PostgreSQL criado automaticamente
- [ ] Deploy realizado com sucesso
- [ ] API funcionando (teste: https://SEU-APP.railway.app/api/health)

### Frontend
- [ ] Vercel conectado ao GitHub
- [ ] Root directory configurado (`rm-papel-frontend`)
- [ ] VITE_API_URL configurado com URL do backend
- [ ] Deploy realizado com sucesso
- [ ] Login funcionando

## 🔧 Configurações Importantes

### Variáveis de Ambiente do Backend
```
SECRET_KEY=rm-papel-secret-key-production-2024
JWT_SECRET_KEY=jwt-secret-string-rm-papel-production
DATABASE_URL=postgresql://... (Railway cria automaticamente)
```

### Variáveis de Ambiente do Frontend
```
VITE_API_URL=https://rm-papel-backend-production.railway.app/api
```

## 🎯 URLs Finais
- **Backend API**: https://rm-papel-backend-production.railway.app
- **Frontend**: https://rm-papel-frontend.vercel.app
- **Documentação**: Disponível nos READMEs de cada pasta

## 🆘 Troubleshooting

### Backend não inicia
- Verifique se as variáveis de ambiente estão configuradas
- Verifique os logs no Railway
- Certifique-se que o Procfile está correto

### Frontend não conecta com Backend
- Verifique se VITE_API_URL está correto
- Verifique se o backend está rodando
- Verifique CORS no backend

### Banco de dados
- Railway cria PostgreSQL automaticamente
- Tabelas são criadas automaticamente na primeira execução
- Para reset: delete o banco no Railway e redeploy

