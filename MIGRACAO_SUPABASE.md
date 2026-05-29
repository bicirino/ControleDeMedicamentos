# 🐘 Migração para PostgreSQL (Supabase) - Guia Completo

**Status:** ✅ Código pronto para PostgreSQL  
**Data:** 29/05/2026

---

## ✅ O que foi feito

- ✅ `database.py` agora suporta **PostgreSQL e SQLite**
- ✅ Detecta automaticamente `DATABASE_URL` (PostgreSQL) ou usa SQLite local
- ✅ Todas as tabelas criadas automaticamente
- ✅ Testes continuam passando (16/16)
- ✅ `requirements.txt` atualizado com `psycopg[binary]`

---

## 🚀 Passo a Passo: Configurar Supabase

### PASSO 1: Criar Projeto no Supabase

1. Acesse https://supabase.com/
2. Clique em **Start your project**
3. Faça login/signup com GitHub ou email
4. Clique em **New Project**
5. Escolha:
   - **Name:** `controle-medicamentos`
   - **Password:** Gere uma senha forte
   - **Region:** Escolha mais próximo (ex: `South America - São Paulo`)
6. Clique em **Create new project**
7. **Aguarde 2-3 minutos** (primeiro projeto demora)

---

### PASSO 2: Obter Connection String

1. Abra seu projeto Supabase
2. Na barra lateral, clique em **Settings** (engrenagem)
3. Clique em **Database**
4. Procure por **Connection String**
5. Escolha a abinha **URI** (não **psql command**)
6. **Copie o valor completo** (exemplo abaixo):

```
postgresql://postgres.xxxxxxxxxxxxx:seu_password@xxxxxxxxxxxxx.supabase.co:5432/postgres?sslmode=require
```

⚠️ **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha que você criou no Passo 1!

---

### PASSO 3: Configurar no Render.com

1. Acesse https://dashboard.render.com
2. Clique em seu serviço `controle-medicamentos`
3. Clique em **Settings** → **Environment**
4. **Adicione/Atualize** estas variáveis:

```
DATABASE_URL = [cole aqui a URI do Supabase]
FLASK_ENV = production
DEBUG = False
SECRET_KEY = [sua chave aleatória de antes]
GROQ_API_KEY = [sua chave Groq de antes]
PYTHON_VERSION = 3.12
```

**Deixe como estava (ou remova):**
```
❌ DB_PATH           (não mais necessário)
```

5. Clique em **Save**

---

### PASSO 4: Fazer Deploy

1. Dashboard Render.com → seu serviço
2. Clique em **Manual Deploy**
3. Selecione **Deploy latest commit**
4. **Aguarde 3-5 minutos**

---

## ✅ Verificação Pós-Deploy

### 1. Acesse a URL do Render
Deve carregar normalmente (tela de login)

### 2. Criar uma Conta
- Email: `teste@example.com`
- Nome: `Teste`
- Senha: `senha123`
- Clique em Registrar

### 3. Fazer Login
- Use a conta criada
- Deve entrar na aplicação

### 4. Cadastrar Medicamento
- Nome: `Dipirona`
- Dosagem: `500mg`
- Horário: `09:00`
- Dia: `todos`
- Clique em Salvar

### 5. Verificar no Supabase (Confirmação!)
1. Abra seu projeto Supabase
2. Clique em **SQL Editor** (barra lateral)
3. Execute:
   ```sql
   SELECT * FROM usuarios;
   SELECT * FROM medicamentos;
   ```
4. ✅ **Você deve ver seus dados lá!**

---

## 🔄 Dados Persistem em Produção?

**Teste crítico:**

1. Cadastre um medicamento no Render
2. Recarregue a página (F5)
3. ✅ Medicamento ainda está?
4. Feche o navegador completamente
5. Abra novamente e faça login
6. ✅ Medicamento ainda está?

Se tudo passa, seus dados estão **100% persistindo no Supabase**! 🎉

---

## 📊 Monitorar Banco de Dados

### Ver Dados em Tempo Real

1. Dashboard Supabase → projeto
2. Clique em **Table Editor** (barra lateral)
3. Você vê as tabelas:
   - `usuarios`
   - `medicamentos`
   - `registros_tomados`

### Executar Queries SQL

1. **SQL Editor** na Supabase
2. Exemplo:
   ```sql
   -- Ver todos os usuários
   SELECT id, email, nome FROM usuarios;
   
   -- Ver medicamentos de um usuário
   SELECT * FROM medicamentos WHERE usuario_id = 1;
   
   -- Ver registros de medicamentos tomados
   SELECT * FROM registros_tomados;
   ```

---

## 🆘 Troubleshooting

### Erro: "Connection refused"
**Causa:** `DATABASE_URL` incorreta  
**Solução:**
1. Verifique se copou a URI completa do Supabase
2. Verifique se tem `[YOUR-PASSWORD]` substituído
3. Teste a conexão localmente:
   ```bash
   psql [DATABASE_URL]
   ```

### Erro: "FATAL: password authentication failed"
**Causa:** Senha errada na URI  
**Solução:**
1. Abra Supabase Dashboard
2. Settings → Database → veja a senha
3. Atualize `DATABASE_URL` no Render

### Banco criou mas está vazio
**Causa:** Aplicação criou schema mas não inseriu dados  
**Solução:**
1. Verifique se dados foram inseridos via UI do Render
2. Confira nos logs: `Render → Logs`

### Erro: "table users does not exist"
**Causa:** Schema não foi criado  
**Solução:**
1. Redeploy: Dashboard → Manual Deploy
2. Deixe criar as tabelas automaticamente

---

## 📈 Performance & Backups

### Backups Automáticos (Supabase)
✅ Supabase faz backup diário automático gratuitamente

### Ver Backups
1. Dashboard Supabase → Settings → Backups
2. Você vê histórico de backups

### Restaurar Backup
1. Settings → Backups
2. Clique no backup desejado
3. Clique em **Restore**

---

## 🔄 Voltar para SQLite (Se Necessário)

Se quiser voltar para SQLite local:

1. Remove `DATABASE_URL` do Render
2. Redeploy
3. App volta a usar `/var/data/medicamentos.db`

---

## 🎯 Próximos Passos

### ✅ Agora você tem:
- ✅ Aplicação em produção
- ✅ Banco PostgreSQL gerenciado (Supabase)
- ✅ Backups automáticos
- ✅ Dashboard para ver dados

### 🚀 Ideias para o Futuro:
- [ ] Adicionar alertas por email
- [ ] Painel admin
- [ ] Exportar dados em PDF
- [ ] Integração com WhatsApp/SMS
- [ ] App mobile

---

## ✅ Confirmação Final

Se tudo passou nos testes acima, você tem:

✅ **Aplicação em produção no Render**  
✅ **Banco de dados PostgreSQL no Supabase**  
✅ **Dados persistindo na nuvem**  
✅ **Backups automáticos**  
✅ **Pronto para escalar!** 🚀

---

**Dúvidas?** Consulte a documentação:
- Supabase: https://supabase.com/docs
- Render: https://render.com/docs
- PostgreSQL: https://www.postgresql.org/docs/
