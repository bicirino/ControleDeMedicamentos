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

### APIs Integradas 🔗

- **BrasilAPI** - Busca de dados sobre medicamentos registrados na ANVISA
- **OpenWeather** - Informações de clima para contexto de saúde do usuário

---

## 📁 Estrutura do Projeto

```
ControleDeMedicamentos/
├── main.py                          # Ponto de entrada e interface CLI
├── medicamentos.py                  # Lógica de negócio
├── database.py                      # Gerenciamento de banco de dados
├── api_integration.py               # Integração com APIs externas (BrasilAPI, OpenWeather)
├── requirements.txt                 # Dependências do projeto
├── .env.example                     # Exemplo de variáveis de ambiente
├── README.md                        # Este arquivo
├── LICENSE                          # Licença MIT
├── CHANGELOG.md                     # Histórico de versões
├── .github/
│   └── workflows/
│       └── ci.yml                   # Pipeline de CI/CD
├── tests/
│   ├── __init__.py
│   ├── test_medicamentos.py         # Testes unitários (11 testes)
│   └── test_api_integration.py      # Testes de integração com APIs (12 testes)
└── .gitignore
```

---

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

Execute o aplicativo no terminal:

```bash
python main.py
```

---

## 📖 Como Usar

### Menu Principal

Ao iniciar, você verá este menu:

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

### Exemplos de Uso

#### 1️⃣ Cadastrar Medicamento

- Escolha a opção **1**
- Digite o nome: `Paracetamol`
- Digite a dosagem: `500mg`
- Digite o horário (HH:MM): `08:00`

#### 2️⃣ Ver Medicamentos do Dia

- Escolha a opção **2**
- Visualize todos os medicamentos para hoje com status (Pendente/Tomado)

#### 3️⃣ Marcar Medicamento como Tomado

- Escolha a opção **3**
- Verá a lista de medicamentos do dia
- Digite o ID do medicamento tomado
- Sistema registra a tomada

#### 4️⃣ Ver Todos os Medicamentos

- Escolha a opção **4**
- Visualize todos os medicamentos cadastrados (Ativos/Inativos)

#### 5️⃣ Remover Medicamento

- Escolha a opção **5**
- Sistema lista todos os medicamentos
- Digite o ID e confirme (s/n)

#### 6️⃣ Consultar Informações de Medicamento (BrasilAPI)

- Escolha a opção **6**
- Digite o nome do medicamento (ex: "Paracetamol")
- Sistema busca informações na BrasilAPI e exibe:
  - 📋 Nome completo
  - 🧪 Princípio ativo
  - 🏢 Laboratório fabricante
  - 📍 CNPJ do medicamento

---

## 🔐 Configuração de Variáveis de Ambiente

### Passo 1: Copiar o arquivo de exemplo

```bash
cp .env.example .env
```

### Passo 2: Configurar chaves de API (opcional)

O arquivo `.env` contém:

```env
# OpenWeather API Key (obtenha em: https://openweathermap.org/api)
OPENWEATHER_API_KEY=sua_chave_aqui

DEBUG=False
```

**Para usar a busca de clima:**

1. Acesse [openweathermap.org/api](https://openweathermap.org/api)
2. Crie uma conta (plano free disponível)
3. Gere uma API Key
4. Adicione no arquivo `.env`

> **Nota:** A BrasilAPI é pública e não requer chave de autenticação.

---

## 🧪 Testes Automatizados

### Executar Todos os Testes

```bash
python -m pytest tests/ -v
```

### Executar Apenas Testes de Integração

```bash
python -m pytest tests/test_api_integration.py -v
```

### Executar Apenas Testes Unitários

```bash
python -m pytest tests/test_medicamentos.py -v
```

### Resultado Esperado

```
23 passed in 0.75s
✅ 11 testes unitários + 12 testes de integração
```

### Cobertura de Testes

**Testes Unitários (11):**

| Categoria | Testes | Descrição |
|-----------|--------|-----------|
| **Cadastro** | 3 | Dados válidos, nome vazio, horário inválido |
| **Listagem Diária** | 3 | Banco vazio, pendentes, tomados |
| **Marcar Tomado** | 3 | Válido, duplicado, ID inválido |
| **Remoção** | 2 | Com confirmação, sem confirmação |

**Testes de Integração (12):**

| API | Testes | Descrição |
|-----|--------|-----------|
| **BrasilAPI** | 5 | Sucesso, não encontrado, timeout, conexão, HTTP error |
| **OpenWeather** | 4 | Sucesso, sem chave, timeout, conexão |
| **Validação** | 3 | Conexão sucesso, servidor indisponível, erro conexão |

> **Note:** Os testes de integração usam `unittest.mock` para simular requisições HTTP sem depender da disponibilidade das APIs.

---

## 🔍 Linting e Qualidade de Código

### Executar Flake8

```bash
python -m flake8 tests/ main.py database.py medicamentos.py --max-line-length=79
```

**Status:** ✅ Sem erros

---

## 📋 CI/CD com GitHub Actions

Este projeto utiliza **GitHub Actions** para automação contínua:

### Pipeline Automática

A cada `push` ou `pull request` na branch `main`, o workflow executa:

1. **Instalação de dependências**
2. **Linting com Flake8** (garantindo padrão de código)
3. **Testes com Pytest** (validando funcionamento)

### Arquivo de Configuração

Consulte [.github/workflows/ci.yml](.github/workflows/ci.yml) para detalhes.

---

## 📝 Controle de Versão

Este projeto segue **Versionamento Semântico** (SemVer):

- **MAJOR**: Mudanças grandes ou incompatíveis
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções menores

**Versão Atual:** `1.0.0`

Para histórico de versões, consulte [CHANGELOG.md](CHANGELOG.md).

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






