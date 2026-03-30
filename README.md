# 💊 Controle De Medicamentos 
- Software de controle de medicamentos e horários para idosos ou pessoas que necessitam de apoio para rotina de medicação; 

## 📖 Sobre o projeto
Este projeto foi desenvolvido como desafio para matéria de Bootcamp da minha faculdade - UniCEUB. O objetivo é criar uma aplicação simples que mitigue uma dor real da sociedade; 

### 🚩 O problema: 
- Idosos frequentemente possuem rotinas complexas de medicação. O esquecimento ou a confusão com os horários pode levar a falhas no tratamento ou riscos de superdosagem acidental.

### 🔎 A solução: 
- Uma aplicação CLI direta e acessível que permite o cadastro de medicamentos e horários, exibindo uma lista clara do que deve ser tomado no dia, auxiliando o idoso e seus cuidadores.

## ⚙️ Tecnologias Utilizadas
1. **Linguagem:** Python; 
2. **Interface:** CLI; 
3. **Armazenamento:** SQLite; 
4. **Testes:** Pytest; 
5. **Linting:** Flake8 

## 📁 Estrutura do Projeto 

## 📦 Instalação e Dependências 
Certifique-se de ter o Python instalado em sua máquina; 

1. Clone o repositório: 
``` git clone https://github.com/bicirino/ControleDeMedicamentos.git``` 
``` cd ControledDeMedicamentos``` 
2. Instale as dependências: 
No terminal: ``` pip install -r requirements.txt ``` 

## 🚀 Como Executar: 
No terminal: ``` python main.py ``` 

## 🛠️ Como Usar
- No menu principal, escolha a opção "1. Cadastrar Medicamento".
- Insira o nome, dosagem e horário.
- Escolha a opção "2. Ver Medicamentos do Dia" para checar a agenda.
- Escolha "3. Marcar como Tomado" após ingerir a medicação.

## 🧪 Testes e Qualidade de Código (CI/CD)
- Este projeto utiliza GitHub Actions para Integração Contínua (CI). A cada push ou pull request na branch main, são executados automaticamente:
- Linting/Análise Estática: Garante a padronização e qualidade do código.
- Testes Automatizados: Valida o comportamento das funções principais do sistema.


## 📝 Controle de Versão
- O projeto utiliza o Versionamento Semântico.
**Versão Atual: 1.0.0** 

## 📃 Licença 
- Este projeto utiliza a licença **MIT** - documentada no arquivo *LICENSE*