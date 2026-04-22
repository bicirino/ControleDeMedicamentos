# 💊 Controle De Medicamentos

**Um aplicativo CLI para auxiliar idosos e cuidadores no controle de medicamentos e horários.**

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

Uma aplicação CLI acessível e direta que permite:
- ✅ Cadastro organizado de medicamentos com horários
- ✅ Visualização clara do que deve ser tomado hoje
- ✅ Registro de medicamentos já tomados
- ✅ Listagem completa de medicamentos
- ✅ Remoção (desativação) de medicamentos

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
| **SQLite** | 3 | Banco de dados |
| **Pytest** | 9.0.2 | Testes automatizados |
| **Flake8** | 7.2.0 | Linting e qualidade de código |
| **Requests** | 2.31.0 | Consumo de APIs REST |
| **python-dotenv** | 1.0.0 | Gerenciamento de variáveis de ambiente |

### API Integrada 🔗

- **BrasilAPI** - Busca de dados sobre medicamentos registrados na ANVISA

---

## 📁 Estrutura do Projeto

```
ControleDeMedicamentos/
│
├── 📄 ARQUIVOS PRINCIPAIS
├── main.py                              # Ponto de entrada e interface CLI
├── medicamentos.py                      # Lógica de negócio (cadastro, listagem, etc)
├── database.py                          # Gerenciamento de banco de dados SQLite
├── api_integration.py                   # ⭐ NOVO: Integração com BrasilAPI
│
├── 📦 DEPENDÊNCIAS E CONFIGURAÇÃO
├── requirements.txt                     # Lista de dependências Python
├── .env.example                         # ⭐ NOVO: Exemplo de variáveis de ambiente
├── render.yaml                          # ⭐ NOVO: Configuração para Deploy Render.com
│
├── 📚 DOCUMENTAÇÃO
├── README.md                            # Este arquivo
├── LICENSE                              # Licença MIT
├── CHANGELOG.md                         # Histórico de versões
├── DEPLOY.md                            # ⭐ NOVO: Guia de Deploy
│
├── 🧪 TESTES
├── tests/
│   ├── __init__.py
│   ├── test_medicamentos.py             # 11 testes unitários
│   └── test_api_integration.py          # ⭐ NOVO: 5 testes de integração com BrasilAPI
│
├── 🔧 CONFIGURAÇÃO GIT
├── .github/
│   └── workflows/
│       └── ci.yml                       # Pipeline CI/CD (testes automáticos)
├── .gitignore                           # Arquivos ignorados pelo Git
│
└── 📊 DADOS E CACHE
    ├── medicamentos.db                  # Banco de dados SQLite (gerado na primeira execução)
    └── .pytest_cache/                   # Cache de testes (gerado automaticamente)
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

### Início Rápido

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

# 4. Configurar variáveis de ambiente (opcional)
cp .env.example .env
# Nota: BrasilAPI é pública e não requer configuração

# 5. Executar aplicação
python main.py
```

### Testando as Funcionalidades

#### ✅ Teste 1: Funcionalidades Básicas

```bash
python main.py
# Menu aparece automaticamente
# Escolha opção 1: Cadastrar Medicamento
# - Nome: Paracetamol
# - Dosagem: 500mg
# - Horário: 08:00
# ✅ Confirmação de cadastro
```

#### ✅ Teste 2: Integração com BrasilAPI (NOVO!)

```bash
python main.py
# Escolha opção 6: Consultar Informações de Medicamento (API)
# - Digite: Paracetamol
# ✅ Sistema busca na BrasilAPI e exibe:
#   - Nome completo
#   - Princípio ativo
#   - Laboratório
#   - CNPJ
```

#### ✅ Teste 3: Testes Automatizados

```bash
# Executar todos os testes (19 total)
python -m pytest tests/ -v

# Apenas testes de integração com BrasilAPI (8 testes)
python -m pytest tests/test_api_integration.py -v

# Apenas testes unitários (11 testes)
python -m pytest tests/test_medicamentos.py -v

# Com relatório de cobertura
python -m pytest tests/ -v --cov=. --cov-report=html
```

#### ✅ Teste 4: Validação de Código

```bash
# Verificar estilo de código (Flake8)
python -m flake8 main.py medicamentos.py database.py api_integration.py --max-line-length=79

# ✅ Esperado: Sem erros ou warnings
```

---

## 📖 Como Usar

### Menu Principal Interativo

A aplicação possui um menu interativo no terminal com 7 opções:

```
╔══════════════════════════════════════════════════╗
║         💊 CONTROLE DE MEDICAMENTOS              ║
║         Sua rotina de saúde em dia!              ║
╚══════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────┐
│                   MENU PRINCIPAL                 │
├──────────────────────────────────────────────────┤
│  1. Cadastrar Medicamento                        │
│  2. Ver Medicamentos do Dia                      │
│  3. Marcar Medicamento como Tomado               │
│  4. Ver Todos os Medicamentos Cadastrados        │
│  5. Remover Medicamento                          │
│  6. Consultar Informações de Medicamento (API)   │
│  0. Sair                                         │
└──────────────────────────────────────────────────┘
```

### Guia Detalhado das Funcionalidades

#### 1️⃣ Cadastrar Medicamento

**O que faz:** Adiciona um novo medicamento ao sistema com horário de administração.

**Como usar:**
```
Opção: 1
📋 Nome do medicamento: Paracetamol
💊 Dosagem (ex: 500mg, 1 comprimido): 500mg
🕐 Horario de tomar (HH:MM): 08:00
✅ Medicamento 'Paracetamol' cadastrado com sucesso!
```

**Validações:**
- ✅ Nome obrigatório (não pode ficar vazio)
- ✅ Dosagem obrigatória
- ✅ Horário no formato HH:MM (08:00, 14:30, etc)

---

#### 2️⃣ Ver Medicamentos do Dia

**O que faz:** Lista todos os medicamentos a tomar hoje com status (Pendente/Tomado).

**Como usar:**
```
Opção: 2

📅 Medicamentos para hoje (2026-04-22):

  ID   Horario   Medicamento           Dosagem              Status
  ──────────────────────────────────────────────────────────────────
  1    08:00     Paracetamol           500mg                ⏳ Pendente
  2    14:00     Antibiótico           1 comprimido         ✅ Tomado
```

---

#### 3️⃣ Marcar Medicamento como Tomado

**O que faz:** Registra que um medicamento foi tomado hoje.

**Como usar:**
```
Opção: 3
[Lista de medicamentos do dia é exibida]
🔢 Informe o ID do medicamento tomado: 1
✅ 'Paracetamol' marcado como tomado!
```

**Proteções:**
- ✅ Não permite marcar o mesmo medicamento 2x no mesmo dia
- ✅ Valida se o ID existe

---

#### 4️⃣ Ver Todos os Medicamentos Cadastrados

**O que faz:** Lista todos os medicamentos cadastrados (Ativos e Inativos).

**Como usar:**
```
Opção: 4

📋 Todos os medicamentos cadastrados:

  ID   Horario   Medicamento           Dosagem              Situacao
  ──────────────────────────────────────────────────────────────────
  1    08:00     Paracetamol           500mg                🟢 Ativo
  2    14:00     Antibiótico           1 comprimido         🔴 Inativo
```

---

#### 5️⃣ Remover Medicamento

**O que faz:** Desativa um medicamento (soft delete - dados permanecem para histórico).

**Como usar:**
```
Opção: 5
[Lista de medicamentos é exibida]
🔢 Informe o ID do medicamento a remover: 1
⚠️  Deseja remover 'Paracetamol'? (s/n): s
✅ 'Paracetamol' removido com sucesso!
```

**Segurança:**
- ✅ Pede confirmação antes de remover
- ✅ Dados históricos preservados no banco

---

#### 6️⃣ Consultar Informações de Medicamento (API) ⭐ NOVO!

**O que faz:** Busca informações detalhadas sobre um medicamento na **BrasilAPI** (banco de medicamentos ANVISA).

**Como usar:**
```
Opção: 6
📋 Digite o nome do medicamento: Paracetamol

🔍 Buscando informações do medicamento na BrasilAPI...

✅ Informações encontradas:

  📋 Nome: Paracetamol 500mg
  🧪 Princípio Ativo: Paracetamol monoidratado
  🏢 Laboratório: Laboratório XYZ Ltda
  📍 CNPJ: 12.345.678/0001-23
```

**Funcionalidade Nova - Etapa 2:**
- ✅ Integração com **BrasilAPI** (pública, sem autenticação)
- ✅ Acesso a dados oficiais da ANVISA
- ✅ Tratamento de erros (medicamento não encontrado, falha de conexão)
- ✅ 5 testes de integração específicos para essa funcionalidade

---

### Fluxo Completo de Uso

1. **Executar**: `python main.py`
2. **Cadastrar**: Opção 1 - Adicionar novo medicamento
3. **Consultar API**: Opção 6 - Verificar informações na BrasilAPI
4. **Ver Hoje**: Opção 2 - Visualizar medicamentos do dia
5. **Marcar**: Opção 3 - Registrar medicamentos tomados
6. **Listar Todos**: Opção 4 - Ver histórico completo
7. **Sair**: Opção 0 - Encerrar aplicação

---

## 🔐 Configuração de Variáveis de Ambiente

A aplicação funciona **100% sem configuração**! BrasilAPI é uma API pública e não requer autenticação.

Você pode copiar o arquivo de exemplo se desejar:

```bash
cp .env.example .env
```

Pronto! ✅ 

---

## 🧪 Testes Automatizados

### Por Que Testes?

Os testes garantem que a aplicação:
- ✅ Funciona corretamente em todos os cenários
- ✅ Integra com APIs sem quebrar
- ✅ Segue padrões de qualidade
- ✅ Pode ser alterada com segurança no futuro

### Como Executar Testes

#### 1. Todos os Testes (23 total)

```bash
python -m pytest tests/ -v

# Saída esperada:
# ============================= test session starts =============================
# collected 23 items
# tests/test_api_integration.py::TestBrasilAPI::test_buscar_medicamento_sucesso PASSED
# tests/test_medicamentos.py::TestCadastrarMedicamento::test_cadastro_valido PASSED
# ...
# ============================= 23 passed in 0.56s ==============================
```

#### 2. Apenas Testes de Integração com APIs (12 testes)

```bash
python -m pytest tests/test_api_integration.py -v

# Valida:
# ✅ Busca na BrasilAPI (5 testes)
# ✅ Busca de clima OpenWeather (4 testes)
# ✅ Validação de conexão (3 testes)
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
python -m flake8 main.py medicamentos.py database.py api_integration.py --max-line-length=79

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

## � Dependências

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

## � Dependências

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

## �🔒 Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Gabriel Martins Cirino**

- GitHub: [@bicirino](https://github.com/bicirino)
- Projeto: [ControleDeMedicamentos](https://github.com/bicirino/ControleDeMedicamentos)






