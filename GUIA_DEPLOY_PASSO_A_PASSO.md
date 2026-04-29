# 🚀 Guia Completo de Deploy - Controle de Medicamentos

**Documento criado em:** 29 de Abril de 2026  
**Versão da aplicação:** Final - Pronta para Deploy  
**Status:** ✅ Todas as correções aplicadas

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Checklist Pré-Deploy](#checklist-pré-deploy)
3. [Configuração do Git](#configuração-do-git)
4. [Setup no Render.com](#setup-no-rendercom)
5. [Monitoramento Pós-Deploy](#monitoramento-pós-deploy)
6. [Troubleshooting](#troubleshooting)

---

## 📋 Pré-requisitos

Antes de iniciar o deploy, certifique-se de que você tem:

- [ ] **Conta GitHub** (com o repositório `ControleDeMedicamentos`)
- [ ] **Conta Render.com** (crie gratuitamente em [render.com](https://render.com))
- [ ] **Conta Groq** (para API de medicamentos em [console.groq.com](https://console.groq.com/))
- [ ] **Git instalado** em sua máquina
- [ ] **Acesso ao repositório GitHub** (se privado)

---

## ✅ Checklist Pré-Deploy

Execute os seguintes passos **antes** de fazer deploy:

### 1️⃣ Verificar Status Local

```bash
# Navegar até o diretório do projeto
cd C:\Users\User\Desktop\Programas e estudos\Python\ControleDeMedicamentos

# Verificar status do git
git status

# Verificar se há mudanças não commitadas
git log --oneline -5  # Ver últimos 5 commits
```

**O que esperar:**
- Nenhuma mudança não commitada
- Todos os arquivos importantes estão versionados

### 2️⃣ Verificar Arquivos Críticos

Os seguintes arquivos **devem** estar presentes no repositório:

```
✅ app.py                 (aplicação Flask)
✅ requirements.txt       (dependências Python)
✅ render.yaml           (configuração Render - CORRIGIDO)
✅ DEPLOY.md             (guia deploy)
✅ .gitignore            (para não versionare .env)
✅ static/               (CSS e JavaScript)
✅ templates/            (HTML)
✅ database.py           (camada banco dados)
✅ medicamentos.py       (lógica de negócio)
✅ api_integration.py    (integração Groq)
```

### 3️⃣ Testar Localmente

```bash
# 1. Instalar dependências em ambiente limpo (recomendado)
python -m venv venv
venv\Scripts\activate

# 2. Instalar from requirements.txt
pip install -r requirements.txt

# 3. Executar testes
pytest tests/ -v

# 4. Iniciar servidor local
python app.py

# 5. Acessar http://127.0.0.1:5000 no navegador
# - Verificar se interface carrega
# - Testar cadastro de medicamento
# - Testar busca com Groq
```

**Esperado:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

### 4️⃣ Verificar Variáveis de Ambiente

O arquivo `.env` **NÃO** deve estar no Git (verificar `.gitignore`):

```bash
# Verificar .gitignore
cat .gitignore | grep .env

# Esperado:
# .env
# .env.local
```

**⚠️ IMPORTANTE:** A chave `GROQ_API_KEY` está em `.env` local, mas será configurada separadamente no Render.

### 5️⃣ Fazer Commit das Mudanças

```bash
# Ver mudanças
git status

# Adicionar todas as mudanças
git add .

# Commit com mensagem descritiva
git commit -m "Correção: render.yaml - usar app.py ao invés de main.py"

# Verificar se commit foi criado
git log --oneline -1
```

---

## 🔧 Configuração do Git

### Preparar o Repositório

```bash
# 1. Estar na branch main (ou sua branch de deploy)
git branch -v

# 2. Se precisar mudar de branch
git checkout main

# 3. Fazer pull das últimas mudanças
git pull origin main

# 4. Verificar remoto está correto
git remote -v
# Esperado:
# origin  https://github.com/SEU-USUARIO/ControleDeMedicamentos.git (fetch)
# origin  https://github.com/SEU-USUARIO/ControleDeMedicamentos.git (push)

# 5. Push das mudanças (se houver)
git push origin main
```

---

## 🎯 Setup no Render.com

### Etapa 1: Acessar Render.com e Criar Web Service

1. **Acesse:** [render.com](https://render.com)
2. **Faça login** com sua conta (ou crie uma nova)
3. **Clique em:** `New +` (canto superior direito)
4. **Selecione:** `Web Service`

### Etapa 2: Conectar Repositório GitHub

1. **Selecione:** "Deploy an existing project from a Git repository"
2. **Clique em:** "Connect a repository"
3. **Se não estiver conectado:**
   - Clique em "GitHub" e autorize Render para acessar seus repos
   - Confirme as permissões

4. **Procure** pelo repositório `ControleDeMedicamentos`
5. **Clique em:** `Select Repository`

### Etapa 3: Configurar Web Service

Preencha os campos exatamente como abaixo:

| Campo | Valor | Notas |
|-------|-------|-------|
| **Name** | `controle-medicamentos` | Será parte da URL pública |
| **Environment** | `Python 3` | Automático |
| **Build Command** | `pip install -r requirements.txt` | Instala dependências |
| **Start Command** | `python app.py` | ✅ CORRIGIDO (era main.py) |
| **Plan** | `Free` | Plano gratuito |

**Exemplo de URL gerada:**
```
https://controle-medicamentos.onrender.com
```

### Etapa 4: Adicionar Variáveis de Ambiente

Na seção **"Environment"**, clique em **"Add Environment Variable"** e adicione:

#### Variable 1: GROQ_API_KEY

| Campo | Valor |
|-------|-------|
| **Key** | `GROQ_API_KEY` |
| **Value** | `sua_chave_aqui` |

**Como obter a chave:**

1. Acesse [console.groq.com](https://console.groq.com/)
2. Crie uma conta (gratuitamente)
3. No dashboard, clique em "API Keys"
4. Clique em "Create New API Key"
5. Copie a chave gerada
6. Cole no campo "Value" do Render

#### Variable 2: DEBUG

| Campo | Valor |
|-------|-------|
| **Key** | `DEBUG` |
| **Value** | `False` |

**Motivo:** Desativar modo debug em produção (segurança)

#### Variable 3: PYTHON_VERSION (Opcional)

| Campo | Valor |
|-------|-------|
| **Key** | `PYTHON_VERSION` |
| **Value** | `3.12` |

### Etapa 5: Revisar Configuração

Sua tela deve parecer com:

```
Name: controle-medicamentos
Environment: Python 3
Region: [Selecionado automaticamente]
Branch: main (ou sua branch)

Build Command: pip install -r requirements.txt
Start Command: python app.py

Environment Variables:
  GROQ_API_KEY: gsk_... (sua chave)
  DEBUG: False
  PYTHON_VERSION: 3.12

Plan: Free
```

### Etapa 6: Deploy

1. **Clique em:** `Create Web Service`
2. **Aguarde:** O build começará automaticamente (2-5 minutos)
3. **Monitore:** Os logs aparecerão na tela

**Esperado durante o build:**
```
[Build] Installing dependencies...
[Build] Collecting flask>=3.0.0...
...
[Build] Running python app.py
[Deploy] Service deployed successfully
```

---

## 📊 Monitoramento Pós-Deploy

### Verificar Status do Deploy

1. **Acesse** o painel do Render.com
2. **Clique** em seu serviço `controle-medicamentos`
3. **Verifique** o status:
   - 🟢 Verde = **Ativo e funcionando**
   - 🟡 Amarelo = **Iniciando/Dormindo**
   - 🔴 Vermelho = **Erro**

### Testar Aplicação Publicada

```bash
# Copiar a URL do serviço (ex: https://controle-medicamentos.onrender.com)
# Abrir em um navegador
```

**Coisas a testar:**

✅ Página carrega sem erros  
✅ Interface dark mode funciona  
✅ Cadastrar novo medicamento  
✅ Consultar medicamentos do dia  
✅ Buscar medicamento via Groq API  
✅ Editar medicamento (aba Todos)  
✅ Tema persiste após reload  

### Ver Logs do Deploy

1. No painel do serviço, clique em **"Logs"**
2. Scroll para cima para ver o histórico do build
3. Procure por mensagens de erro (linhas vermelhas)

**Exemplo de logs saudáveis:**
```
2026-04-29 10:30:45 Building image...
2026-04-29 10:31:02 Successfully built image
2026-04-29 10:31:05 Starting service...
2026-04-29 10:31:10 Service started on port 5000
2026-04-29 10:31:12 Ready to accept requests
```

### Métricas e Monitoramento

1. Clique em **"Metrics"** (próximo a Logs)
2. Monitore:
   - **CPU Usage** - Deve estar baixo (< 50%)
   - **Memory Usage** - Deve estar baixo (< 200MB)
   - **Requests** - Monitore atividade

---

## 🔄 Deploy Automático

Após configurar, o deploy é **automático**:

- Qualquer `push` em `main` acionará novo deploy automaticamente
- Tempo de deploy: 2-5 minutos

### Fazer Deploy Manual

Se precisar fazer deploy sem fazer push:

1. No painel Render.com
2. Clique em **"Manual Deploy"**
3. Selecione **"Deploy latest commit"**
4. Aguarde conclusão

---

## 🔐 Segurança - Boas Práticas

Antes de considerar o deploy bem-sucedido, verifique:

- ✅ `.env` **NÃO** está no repositório Git
- ✅ Variáveis sensíveis estão **APENAS** no Render.com
- ✅ `DEBUG=False` em produção
- ✅ Arquivo `render.yaml` está correto (`app.py`, não `main.py`)
- ✅ `requirements.txt` está atualizado
- ✅ Todas as dependências estão listadas

---

## 🆘 Troubleshooting

### ❌ Erro: "ModuleNotFoundError: No module named 'groq'"

**Causa:** Dependência não listada em requirements.txt  
**Solução:**

```bash
# Verificar requirements.txt contém:
# groq>=0.4.1

# Se falta, adicionar:
echo "groq>=0.4.1" >> requirements.txt

# Commit e push
git add requirements.txt
git commit -m "Adicionar groq ao requirements.txt"
git push origin main

# No Render: Manual Deploy > Deploy latest commit
```

### ❌ Erro: "GROQ_API_KEY não está definido"

**Causa:** Variável de ambiente não configurada no Render  
**Solução:**

1. No painel Render, abra seu serviço
2. Clique em **"Environment"**
3. Verifique se `GROQ_API_KEY` está listado
4. Se não estiver, clique em **"Add Environment Variable"**
5. Adicione: `Key: GROQ_API_KEY`, `Value: gsk_...`
6. Clique em **"Save"** e aguarde redeploy

### ❌ Erro: "Application is starting" (página branca)

**Causa:** Aplicação ainda está iniciando ou crashing  
**Solução:**

1. Aguarde 1-2 minutos
2. Recarregue a página (F5)
3. Se persistir, verifique logs (ver Logs do Deploy)

### ❌ Serviço desceu após 15 minutos (Free Plan)

**Causa:** Plano Free hiberna após 15 min de inatividade  
**Soluções:**

**Opção 1 - Aceitar dormência (gratuito):**
- Primeira requisição acordará o serviço (demora 30 segundos)

**Opção 2 - Upgrade para plano Pro (pago):**
- 1. No painel Render, clique em **"Settings"**
- 2. Clique em **"Change Plan"**
- 3. Selecione **"Standard"** ou **"Pro"**
- 4. Configure o período de faturamento

### ❌ Erro: "Build failed"

**Causa:** Erro durante instalação de dependências  
**Solução:**

1. Acesse os logs (**"Logs"**)
2. Procure pela mensagem de erro específica
3. Teste localmente:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
4. Corrija o erro local
5. Commit, push e redeploy

### ❌ Medicamentos não aparecem ou erro de busca

**Causa:** Problema com Groq API  
**Solução:**

1. Verificar se `GROQ_API_KEY` está correta:
   - Acesse [console.groq.com](https://console.groq.com/)
   - Verifique se a chave ainda é válida
   - Gere uma nova chave se necessário
   
2. Atualizar no Render:
   - Painel > Seu serviço > Environment
   - Atualizar `GROQ_API_KEY`
   - Clique "Save" e aguarde redeploy

3. Testar novamente a busca

---

## 📝 Resumo do Deploy

| Etapa | Status | Notas |
|-------|--------|-------|
| 1. Verificar pré-requisitos | ✅ | GitHub, Render, Groq |
| 2. Testar localmente | ✅ | `python app.py` funcionando |
| 3. Fazer commit e push | ✅ | `git push origin main` |
| 4. Criar Web Service no Render | ✅ | Conectar repositório |
| 5. Configurar variáveis | ✅ | GROQ_API_KEY, DEBUG, PYTHON_VERSION |
| 6. Deploy | ✅ | Clicar "Create Web Service" |
| 7. Monitorar build | ✅ | Verificar logs (2-5 min) |
| 8. Testar aplicação publicada | ✅ | Validar funcionalidades |
| 9. Monitoramento contínuo | ✅ | Verificar métricas |

---

## 🎉 Aplicação em Produção!

Após completar todos os passos:

✅ Aplicação está **online** e **acessível** publicamente  
✅ Deploy automático ativado para mudanças futuras  
✅ Variáveis sensíveis protegidas  
✅ Pronto para uso em produção  

---

## 📞 Próximos Passos

- [ ] Compartilhar URL com usuários finais
- [ ] Monitorar logs regularmente
- [ ] Criar rotina de backup de dados
- [ ] Configurar alertas de falha (opcional - Free Plan)
- [ ] Documentar mudanças no CHANGELOG.md

---

**Deploy finalizado com sucesso! 🚀**

*Para dúvidas, consulte DEPLOY.md ou [Render Docs](https://render.com/docs)*
