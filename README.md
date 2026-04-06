# 💊 Controle De Medicamentos

**Um aplicativo CLI para auxiliar idosos e cuidadores no controle de medicamentos e horários.**

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

---

## 📁 Estrutura do Projeto

```
ControleDeMedicamentos/
├── main.py                          # Ponto de entrada e interface CLI
├── medicamentos.py                  # Lógica de negócio
├── database.py                      # Gerenciamento de banco de dados
├── requirements.txt                 # Dependências do projeto
├── README.md                        # Este arquivo
├── LICENSE                          # Licença MIT
├── CHANGELOG.md                     # Histórico de versões
├── .github/
│   └── workflows/
│       └── ci.yml                   # Pipeline de CI/CD
├── tests/
│   ├── __init__.py
│   └── test_medicamentos.py         # Testes automatizados (11 testes)
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

---

## 🧪 Testes Automatizados

### Executar Todos os Testes

```bash
python -m pytest tests/ -v
```

### Resultado Esperado

```
11 passed in 0.23s
✅ Todos os testes cobrem:
- Cadastro válido e inválido
- Listagem de medicamentos
- Marcação como tomado (incluindo duplicatas)
- Remoção com confirmação
```

### Cobertura de Testes

Os **11 testes** cobrem:

| Categoria | Testes | Descrição |
|-----------|--------|-----------|
| **Cadastro** | 3 | Dados válidos, nome vazio, horário inválido |
| **Listagem Diária** | 3 | Banco vazio, pendentes, tomados |
| **Marcar Tomado** | 3 | Válido, duplicado, ID inválido |
| **Remoção** | 2 | Com confirmação, sem confirmação |

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

## 📄 Dependências

Todas as dependências estão explicitamente declaradas em `requirements.txt`:

```
pytest==9.0.2
flake8==7.2.0
```

---

## 🔒 Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Gabriel Martins Cirino**

- GitHub: [@bicirino](https://github.com/bicirino)
- Projeto: [ControleDeMedicamentos](https://github.com/bicirino/ControleDeMedicamentos)

---

## 🔗 Links Úteis

- 📦 Repositório: [github.com/bicirino/ControleDeMedicamentos](https://github.com/bicirino/ControleDeMedicamentos)
- 📝 Issues: [Reportar problemas](https://github.com/bicirino/ControleDeMedicamentos/issues)
- 📌 Releases: [Versões do projeto](https://github.com/bicirino/ControleDeMedicamentos/releases)

---

## 💡 Contribuições

Sugestões e melhorias são bem-vindas! Se você tiver ideias para melhorar este projeto:

1. Faça um fork
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## ❓ FAQ

**P: Meus dados estão salvos?**
R: Sim! Os medicamentos são salvos em um banco SQLite local (`medicamentos.db`).

**P: Posso usar em múltiplos dispositivos?**
R: Atualmente, o banco é local. Para múltiplos dispositivos, seria necessário integração com um servidor.

**P: Como removo um medicamento sem perder o histórico?**
R: O sistema usa "soft delete" - medicamentos removidos são marcados como inativos mas permanecem no banco.

---

## 📞 Suporte

Se tiver dúvidas ou encontrar problemas, abra uma [issue no GitHub](https://github.com/bicirino/ControleDeMedicamentos/issues).
