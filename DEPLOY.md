# 🚀 Guia de Deploy - Controle de Medicamentos

## Plataforma de Deploy: Render.com

Este guia descreve como fazer deploy da aplicação **Controle de Medicamentos** no Render.com (gratuito).

---

## ✅ Pré-requisitos

1. **Conta GitHub** com o repositório do projeto
2. **Conta Render.com** (crie em [render.com](https://render.com))
3. **Variáveis de Ambiente** configuradas (`.env.example` fornecido)

---

## 📋 Passo a Passo do Deploy

### Etapa 1: Conectar GitHub ao Render.com

1. Acesse [render.com](https://render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Selecione **"Deploy an existing project from a Git repository"**
4. Conecte sua conta GitHub se não estiver conectada
5. Autorize o Render.com para acessar seus repositórios

### Etapa 2: Selecionar o Repositório

1. Procure por **"ControleDeMedicamentos"**
2. Clique em **"Select Repository"**
3. Confirme o branch (deve ser `entrega-intermediaria` ou `main`)

### Etapa 3: Configurar o Web Service

Preencha os campos conforme abaixo:

| Campo | Valor | Descrição |
|-------|-------|-----------|
| **Name** | `controle-medicamentos` | Nome único do serviço |
| **Runtime** | `Python 3` | Selecione Python 3 |
| **Build Command** | `pip install -r requirements.txt` | Instala dependências |
| **Start Command** | `python main.py` | Comando para iniciar a app |
| **Plan** | `Free` | Plano gratuito (dormência após 15min inatividade) |

### Etapa 4: Adicionar Variáveis de Ambiente

1. Na seção **"Environment"**, adicione as variáveis:

```
GROQ_API_KEY=sua_chave_groq_aqui
DEBUG=False
PYTHON_VERSION=3.12
```

2. **Para `GROQ_API_KEY`:**
   - Obtenha uma chave gratuita em [console.groq.com](https://console.groq.com/)
   - A aplicação usa o modelo `llama-3.1-8b-instant` para consultas de medicamentos
   - Copie sua chave API e cole no campo acima

### Etapa 5: Deploy

1. Clique em **"Deploy Web Service"**
2. Aguarde o build completar (2-5 minutos)
3. Quando terminar, você receberá uma **URL pública**

**Exemplo de URL:**
```
https://controle-medicamentos.onrender.com
```

---

## 🔄 Deploy Automático

Após configurar, qualquer `push` na branch escolhida acionará um novo deploy automaticamente.

### Para fazer novo deploy manualmente:

1. Acesse o painel do Render.com
2. Clique no seu serviço
3. Clique em **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📝 Verificar Status do Deploy

1. Acesse a URL do seu serviço
2. Se receber "Application is starting" ou similar, aguarde
3. Aplicação estará pronta quando exibir o menu principal

### Ver Logs do Deploy

1. No painel Render.com
2. Clique em **"Logs"** para ver erros ou status

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'groq'"

**Solução:** Verifique se `requirements.txt` está correto:
```bash
pytest>=9.0.2
flake8>=7.2.0
requests>=2.31.0
python-dotenv>=1.0.0
groq>=0.4.1
```

### Erro: "GROQ_API_KEY não configurada"

**Solução:**
1. Acesse [console.groq.com](https://console.groq.com/)
2. Crie uma conta gratuita
3. Gere uma API Key no dashboard
4. Adicione em variáveis de ambiente no Render.com (seção "Environment")

### Erro: "Medicamento não encontrado" na busca

**Possíveis causas:**
- GROQ_API_KEY expirada ou inválida
- API Groq fora do ar (consulte [status.groq.com](https://status.groq.com))
- Timeout na requisição (tente novamente)

### Serviço desceu após 15 minutos de inatividade

**Nota:** Plano Free do Render.com hiberna após 15 minutos sem requisições.
- Para manter ativo 24/7, upgrade para plano **Pro** (pago)

---

## 📊 Monitoramento

### Ver métricas:

1. No painel do serviço, clique em **"Metrics"**
2. Monitore CPU, memória e requisições

### Alertas:

1. Configure alertas em **"Settings"** → **"Notifications"**
2. Receba notificações de falhas por email

---

## 🔐 Segurança

✅ **Boas práticas:**

- ✅ Nunca commit `.env` (use `.gitignore`)
- ✅ Adicione variáveis sensíveis no painel Render.com
- ✅ Mantenha `requirements.txt` atualizado
- ✅ Use branches protegidas no GitHub

---

## 📱 Testando a Aplicação Publicada

Após deploy:

```bash
# Copiar o link do Render (ex: https://seu-app.onrender.com)
# Acessar a API ou CLI da sua aplicação

# Se usar CLI, clone e execute localmente
git clone https://github.com/seu-usuario/ControleDeMedicamentos
cd ControleDeMedicamentos
pip install -r requirements.txt
python main.py
```

---

## 🆘 Suporte

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** [ControleDeMedicamentos/issues](https://github.com/bicirino/ControleDeMedicamentos/issues)

---

**Deploy realizado com sucesso! 🎉**
