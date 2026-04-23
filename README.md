# 💊 Controle De Medicamentos

**Uma aplicação web moderna para auxiliar idosos e cuidadores no controle de medicamentos e horários.**

> **🌐 Deploy ao Vivo:** [Disponível em breve - link será adicionado após publicação]

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como desafio de Bootcamp para demonstrar práticas modernas de desenvolvimento de software incluindo boas práticas de organização, documentação, testes e integração contínua.

### 🚩 O Problema

Idosos frequentemente enfrentam rotinas complexas de medicação:
- Esquecimento de horários de tomada
- Confusão sobre qual medicamento tomar
- Risco de superdosagem acidental
- Dificuldade dos cuidadores em acompanhar a rotina

### ✨ A Solução

Uma aplicação web moderna e intuitiva que permite:
- ✅ Cadastro organizado de medicamentos com horários
- ✅ Visualização clara do que deve ser tomado hoje
- ✅ Registro de medicamentos já tomados
- ✅ Interface gráfica profissional e acessível
- ✅ Modo claro e escuro automático
- ✅ Totalmente responsivo (desktop, tablet, smartphone)

---

## 👥 Público-Alvo

- Idosos com necessidade de controle de medicação
- Cuidadores de pessoas com rotinas complexas de medicamentos
- Familiares que auxiliam na organização de medicamentos

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|----------|--------|-----|
| **Python** | 3.12 | Linguagem principal |
| **Flask** | 3.0.0+ | Framework web para interface gráfica |
| **SQLite** | 3 | Banco de dados |
| **HTML5** | - | Markup semântico |
| **CSS3** | - | Estilos acessíveis e responsivos |
| **JavaScript** | - | Interatividade da interface |
| **Pytest** | 9.0.2 | Testes automatizados |
| **Flake8** | 7.2.0 | Linting e qualidade de código |
| **Requests** | 2.31.0 | Consumo de APIs REST |
| **python-dotenv** | 1.0.0 | Gerenciamento de variáveis de ambiente |
| **Groq** | 0.4.1+ | IA para informações sobre medicamentos |

### API Integrada 🔗

- **Groq AI** - Busca de dados com Inteligência Artificial sobre medicamentos

---

## 📁 Estrutura do Projeto

```
ControleDeMedicamentos/
│
├── 📄 APLICAÇÃO WEB
├── app.py                               # Servidor Flask (Backend)
│
├── 📄 LÓGICA DE NEGÓCIO
├── medicamentos.py                      # Funções de cadastro, listagem, etc
├── database.py                          # Gerenciamento de banco de dados SQLite
├── api_integration.py                   # Integração com Groq AI
│
├── 🌐 INTERFACE WEB
├── templates/
│   └── index.html                       # Página HTML da interface web
├── static/
│   ├── style.css                        # Estilos responsivos e acessíveis
│   └── script.js                        # Lógica JavaScript e chamadas à API
│
├── 📦 DEPENDÊNCIAS E CONFIGURAÇÃO
├── requirements.txt                     # Lista de dependências Python
├── .env.example                         # Exemplo de variáveis de ambiente
├── render.yaml                          # Configuração para Deploy Render.com
│
├── 📚 DOCUMENTAÇÃO
├── README.md                            # Este arquivo
├── LICENSE                              # Licença MIT
├── CHANGELOG.md                         # Histórico de versões
├── DEPLOY.md                            # Guia para o Deploy
│
├── 🧪 TESTES
├── tests/
│   ├── __init__.py
│   ├── test_medicamentos.py             # Testes unitários
│   └── test_api_integration.py          # Testes de integração com Groq AI
│
├── 🔧 CONFIGURAÇÃO GIT
├── .github/
│   └── workflows/
│       └── ci.yml                       # Pipeline CI/CD (testes automáticos)
├── .gitignore                           # Arquivos ignorados pelo Git
│
└── 📊 DADOS E CACHE
    ├── medicamentos.db                  # Banco de dados SQLite
    └── .pytest_cache/                   # Cache de testes
```



## 📦 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes)

### Passos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/bicirino/ControleDeMedicamentos.git
   cd ControleDeMedicamentos
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Como Executar

### 🌐 Interface Web [RECOMENDADA PARA IDOSOS]

A interface web é a forma mais amigável de usar o sistema, com uma interface gráfica intuitiva e acessível.

```bash
# 1. Clonar repositório
git clone https://github.com/bicirino/ControleDeMedicamentos.git
cd ControleDeMedicamentos

# 2. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # macOS/Linux

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente (necessário para consultas com IA)
cp .env.example .env
# Adicione sua chave Groq (gratuita em: https://console.groq.com/)

# 5. Executar aplicação web
python app.py

# 6. Abrir no navegador
# Acesse: http://localhost:5000
```

**Características da Interface Web:**
- ✅ Design moderno e responsivo
- ✅ Otimizado para idosos (letras grandes, botões grandes)
- ✅ Alto contraste e cores acessíveis
- ✅ Funciona em desktop, tablet e smartphone
- ✅ Sem necessidade de conhecimento técnico

---

## 📖 Como Usar

### Interface Web - Guia de Funcionalidades

A aplicação web possui 4 abas principais para gerenciar seus medicamentos:

#### 📆 Aba 1: Hoje

Mostra todos os medicamentos que precisam ser tomados **hoje**, com status de cada um:
- ✔️ Verde = Já tomado
- ⏳ Cinza = Ainda não tomado

**Como usar:**
1. Clique na aba "📆 Hoje"
2. Veja os medicamentos organizados por horário
3. Clique no medicamento para marcar como tomado
4. Clique no ícone 🗑️ para remover o medicamento

---

#### 📝 Aba 2: Todos

Lista **todos** os medicamentos cadastrados na sua rotina. Aqui você pode:
- Visualizar a lista completa
- Remover medicamentos que não mais precisa tomar
- Ver todos os horários de uma vez

---

#### ✨ Aba 3: Novo

Adiciona um **novo medicamento** ao seu controle:

**Passos:**
1. Clique na aba "✨ Novo"
2. Preencha:
   - **Nome:** Nome do medicamento (ex: Paracetamol)
   - **Dosagem:** Quantidade (ex: 500mg, 1 comprimido)
   - **Horário:** Hora para tomar (ex: 08:00, 14:30)
3. Clique em "Cadastrar"
4. ✅ Medicamento adicionado com sucesso!

---

#### 🔍 Aba 4: Consultar

Busca informações detalhadas sobre um medicamento usando **Inteligência Artificial** (Groq AI):

**Como usar:**
1. Clique na aba "🔍 Consultar"
2. Digite o nome do medicamento (ex: Paracetamol)
3. Clique em "Buscar"
4. 🤖 O sistema consulta a IA e exibe:
   - Nome do medicamento
   - Para que serve
   - Como usar
   - Cuidados e contraindicações

---

### 🌙 Modo Claro/Escuro

A aplicação detecta automaticamente suas preferências:
- **Modo Escuro:** Se seu sistema está em dark mode
- **Modo Claro:** Se seu sistema está em light mode

**Ou escolha manualmente:**
- Clique no ícone ☀️/🌙 no canto superior direito para alternar entre temas

---

## 🔐 Configuração de Variáveis de Ambiente

### Funcionalidade Básica
A aplicação funciona **100% sem configuração** para as abas 1-3 (Hoje, Todos, Novo).

### Funcionalidade de IA (Aba Consultar)
Para usar a consulta de medicamentos com IA, você precisa de uma chave Groq (gratuita):

1. **Obtenha uma chave gratuita:**
   - Acesse: https://console.groq.com/
   - Crie uma conta
   - Copie sua chave de API

2. **Configure no seu ambiente:**
   ```bash
   cp .env.example .env
   # Edite .env e adicione:
   # GROQ_API_KEY=sua_chave_aqui
   ```

3. **Pronto!** ✅ A aba "Consultar" funcionará normalmente

> **Nota:** A chave Groq é **gratuita** e vem com um limite generoso de requisições (suficiente para uso pessoal) 

---

## 🧪 Testes Automatizados

### Por Que Testes?

Os testes garantem que a aplicação:
- ✅ Funciona corretamente em todos os cenários
- ✅ Integra com APIs sem quebrar
- ✅ Segue padrões de qualidade
- ✅ Pode ser alterada com segurança no futuro

### Como Executar Testes

#### 1. Todos os Testes (16 total)

```bash
python -m pytest tests/ -v

# Saída esperada:
# ============================= test session starts =============================
# collected 16 items
# tests/test_api_integration.py::TestGroqAPI::test_buscar_medicamento_sucesso PASSED
# tests/test_medicamentos.py::TestCadastrarMedicamento::test_cadastro_valido PASSED
# ...
# ============================= 16 passed in 0.59s ================================
```

#### 2. Apenas Testes de Integração com IA (5 testes)

```bash
python -m pytest tests/test_api_integration.py -v

# Valida:
# ✅ Busca com Groq AI (5 testes):
#    - Busca bem-sucedida
#    - Medicamento não encontrado
#    - Sem API key configurada
#    - Erro de conexão
#    - Timeout
```

#### 3. Apenas Testes Unitários (11 testes)

```bash
python -m pytest tests/test_medicamentos.py -v

# Valida:
# ✅ Cadastro de medicamentos (3 testes)
# ✅ Listagem (3 testes)
# ✅ Marcar como tomado (3 testes)
# ✅ Remoção (2 testes)
```

#### 4. Com Relatório de Cobertura

```bash
python -m pytest tests/ -v --cov=. --cov-report=html

# Gera arquivo: htmlcov/index.html
# Abre no navegador para ver cobertura detalhada
```

### Detalhes dos Testes

#### 🧪 Testes Unitários (11)

Testam funcionalidades individuais da aplicação:

| Categoria | Testes | Descrição |
|-----------|--------|-----------|
| **Cadastro** | 3 | Dados válidos, nome vazio, horário inválido |
| **Listagem Diária** | 3 | Sem medicamentos, pendentes, tomados |
| **Marcar Tomado** | 3 | Válido, duplicado, ID inválido |
| **Remoção** | 2 | Com confirmação, sem confirmação |

#### 🌐 Testes de Integração (5) ⭐ NOVO

Testam comunicação com BrasilAPI:

| API | Testes | Descrição |
|-----|--------|-----------|
| **BrasilAPI** | 5 | Sucesso, não encontrado, timeout, conexão, erro HTTP |

> **Nota:** Os testes de integração usam `unittest.mock` para simular requisições HTTP, então funcionam sem depender da API estar online.

---


## 🔍 Linting e Qualidade de Código (Flake8)

### Por Que Flake8?

Garante que o código segue padrões Python reconhecidos internacionalmente (PEP 8).

### Executar Flake8

```bash
python -m flake8 medicamentos.py database.py api_integration.py app.py --max-line-length=120

# Saída esperada (NENHUMA):
# (sem erros ou warnings = ✅ sucesso)
```

### Status Atual

✅ **Código 100% compatível com Flake8**

```bash
Status: PASS
Warnings: 0
Errors: 0
Max line length: 79 caracteres ✅
```

---

## 📊 CI/CD com GitHub Actions

Este projeto utiliza **GitHub Actions** para automação contínua:

### O Que Acontece a Cada Push?

```
1. GitHub detecta novo push
   ↓
2. Workflow `.github/workflows/ci.yml` inicia
   ├── Instala Python 3.12
   ├── Instala dependências
   ├── Executa Flake8 (validação de código)
   ├── Executa Pytest (16 testes)
   └── Exibe resultado (✅ ou ❌)
   ↓
3. Resultado aparece no Pull Request
```

### Ver Status do CI

1. Acesse [GitHub Actions](https://github.com/bicirino/ControleDeMedicamentos/actions)
2. Clique no workflow mais recente
3. Veja detalhes de cada etapa

---

## 📝 Versionamento

Este projeto segue **Versionamento Semântico** (SemVer):

### Versão Atual

| Versão | Data | Status | Etapa |
|--------|------|--------|-------|
| **1.0.0** | 2026-04-15 | ✅ Completa | 1 - CLI Básica |
| **1.1.0** | 2026-04-22 | 🚀 Em Progresso | 2 - APIs + Testes |
| **2.0.0** | 📅 Próxima | 📋 Planejada | 3 - Interface Gráfica |

### Formato SemVer

- **MAJOR** (1.0.0 → 2.0.0): Mudanças grandes/incompatíveis (GUI será MAJOR)
- **MINOR** (1.0.0 → 1.1.0): Novas funcionalidades (APIs são MINOR)
- **PATCH** (1.1.0 → 1.1.1): Correções menores

Para histórico completo, veja [CHANGELOG.md](CHANGELOG.md).

---


### Descrição das Dependências

| Pacote | Versão | Razão |
|--------|--------|-------|
| **pytest** | >=9.0.2 | Framework de testes automatizados |
| **flake8** | >=7.2.0 | Linter para validação de código Python |
| **requests** | >=2.31.0 | Consumo de APIs HTTP (BrasilAPI, OpenWeather) |
| **python-dotenv** | >=1.0.0 | Carregamento de variáveis de ambiente do arquivo .env |

---

## Dependências

Todas as dependências estão explicitamente declaradas em `requirements.txt`:

```
pytest>=9.0.2
flake8>=7.2.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### Descrição das Dependências

| Pacote | Versão | Razão |
|--------|--------|-------|
| **pytest** | >=9.0.2 | Framework de testes automatizados |
| **flake8** | >=7.2.0 | Linter para validação de código Python |
| **requests** | >=2.31.0 | Consumo de APIs HTTP (BrasilAPI, OpenWeather) |
| **python-dotenv** | >=1.0.0 | Carregamento de variáveis de ambiente do arquivo .env |

---

## 🚀 Deploy

### Plataforma de Deploy

Este projeto será hospedado em **Render.com** (gratuito para aplicações Python).

**Link do Deploy:** [Será adicionado após publicação]

### Instruções para Deploy

1. Faça o push da branch `entrega-intermediaria` para o GitHub
2. Acesse [render.com](https://render.com)
3. Conecte sua conta GitHub
4. Crie um novo "Web Service"
5. Selecione este repositório
6. Configure as variáveis de ambiente (.env)
7. Deploy será automático a cada push

---

## 🔒 Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Gabriel Martins Cirino**

- GitHub: [@bicirino](https://github.com/bicirino)
- Projeto: [ControleDeMedicamentos](https://github.com/bicirino/ControleDeMedicamentos)






