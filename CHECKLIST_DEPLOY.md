# ✅ Checklist Rápido - Deploy Controle de Medicamentos

Data: 29 de Abril de 2026

---

## 🔴 PRÉ-DEPLOY (Execute Localmente)

```bash
# 1. Status do Git
git status
# ✅ Sem mudanças não commitadas
```

- [ ] Nenhuma mudança pendente

```bash
# 2. Testar Localmente
python app.py
# Abrir http://127.0.0.1:5000 no navegador
```

- [ ] Aplicação roda sem erros
- [ ] Interface carrega corretamente
- [ ] Dark mode funciona
- [ ] Cadastro de medicamento funciona

```bash
# 3. Fazer Commit (se houver mudanças)
git add .
git commit -m "Correção: render.yaml - usar app.py ao invés de main.py"
git push origin main
```

- [ ] Commit enviado ao GitHub

---

## 🟡 RENDER.COM SETUP

### Conectar Repositório

- [ ] Acessado [render.com](https://render.com)
- [ ] Clicado em `New +` > `Web Service`
- [ ] Autorizou GitHub
- [ ] Selecionou repositório `ControleDeMedicamentos`

### Configurar Serviço

- [ ] **Name:** `controle-medicamentos`
- [ ] **Runtime:** `Python 3`
- [ ] **Build Command:** `pip install -r requirements.txt`
- [ ] **Start Command:** `python app.py` ✅ (não main.py)
- [ ] **Plan:** `Free`

### Adicionar Variáveis de Ambiente

**Passo a passo:**
1. Na seção "Environment", clique em "Add Environment Variable"
2. Para cada variável abaixo, repita:

#### Variable 1: GROQ_API_KEY

- [ ] **Key:** `GROQ_API_KEY`
- [ ] **Value:** (sua chave de [console.groq.com](https://console.groq.com/))

#### Variable 2: DEBUG

- [ ] **Key:** `DEBUG`
- [ ] **Value:** `False`

#### Variable 3: PYTHON_VERSION (Opcional)

- [ ] **Key:** `PYTHON_VERSION`
- [ ] **Value:** `3.12`

---

## 🟢 DEPLOY

- [ ] Clicado em **"Create Web Service"**
- [ ] Aguardou conclusão do build (2-5 minutos)
- [ ] Verificou logs - sem erros 🟢
- [ ] Obteve URL pública (ex: `https://controle-medicamentos.onrender.com`)

---

## ✅ PÓS-DEPLOY (Validação)

```
Acessar: https://seu-app.onrender.com
```

- [ ] Página inicial carrega
- [ ] Dark mode funciona
- [ ] **Teste 1:** Cadastrar novo medicamento
  - Preencher nome, dosagem, horário
  - Selecionar dia
  - Clicar "Salvar"
  - ✅ Medicamento aparece na lista

- [ ] **Teste 2:** Consultar medicamento via Groq
  - Na aba "Consultar", digitar nome de um medicamento
  - Clicar "Buscar"
  - ✅ Informações aparecem corretamente

- [ ] **Teste 3:** Editar medicamento
  - Ir para aba "Todos"
  - Clicar em medicamento
  - Editar informação
  - ✅ Mudança salva corretamente

- [ ] **Teste 4:** Theme persiste
  - Alternar para dark mode
  - Recarregar página (F5)
  - ✅ Permanece em dark mode

---

## 📊 MONITORAMENTO

- [ ] Acessado painel Render.com
- [ ] Verificado status: 🟢 (verde)
- [ ] Verificado **Logs** - sem erros
- [ ] Verificado **Metrics** - CPU/Memory baixos

---

## 🎉 DEPLOY CONCLUÍDO!

```
URL de Acesso:
https://controle-medicamentos.onrender.com

Compartilhado com:
- [ ] Equipe
- [ ] Usuários finais
- [ ] Stakeholders
```

---

## 🔄 Para Futuros Deploys

Sempre que fizer mudanças:

```bash
# 1. Testar localmente
python app.py

# 2. Commit e push
git add .
git commit -m "Descrição da mudança"
git push origin main

# 3. Deploy automático acontecerá
# (Nenhuma ação necessária no Render)
```

---

## 🆘 Problema?

Consulte a seção **Troubleshooting** em: `GUIA_DEPLOY_PASSO_A_PASSO.md`

---

**Boa sorte! 🚀**
