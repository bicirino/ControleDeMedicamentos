# Changelog

Todos às mudanças notáveis neste projeto terão documentação neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto respeita o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-04-10

### ✨ Adicionado

- **Interface CLI completa** com menu interativo e navegação intuitiva
- **Sistema de cadastro de medicamentos** com validação de dados:
  - Nome do medicamento
  - Dosagem (ex: 500mg, 1 comprimido)
  - Horário de administração (validação HH:MM)
- **Visualização de medicamentos do dia** com status (Pendente/Tomado)
- **Registro de medicamentos tomados** com rastreamento de data
- **Listagem completa** de medicamentos (Ativos/Inativos)
- **Remoção segura de medicamentos** com confirmação
- **Banco de dados SQLite** para persistência local
- **Testes automatizados** (11 testes cobrindo casos válidos, inválidos e limites)
- **Linting com Flake8** para qualidade de código
- **GitHub Actions CI** para validação automática
- **Documentação completa** com README, instrções de instalação e uso
- **Licença MIT** para uso livre

### 🔄 Design da Solução

O projeto resolve a dor real de idosos e cuidadores que enfrentam:
- Esquecimento de horários de medicação
- Confusão sobre qual medicamento tomar
- Risco de superdosagem acidental
- Dificuldade em acompanhar a rotina

A solução oferece uma interface simples, acessível e funcional que ajuda na:
- Organização centralizada de medicamentos
- Consulta rápida do que deve ser tomado hoje
- Registro confiável de medicações já realizadas

### 🏛️ Estrutura Técnica

- **Linguagem**: Python 3.12
- **Banco de Dados**: SQLite 3
- **Framework de Testes**: pytest
- **Linting**: flake8
- **CI/CD**: GitHub Actions

---

## [Não Lançado]

### Futuras Melhorias Planejadas

- [ ] Implementação de interface gráfica 
- [ ] Integração com servidor para múltiplos dispositivos
- [ ] Notificações/alarmes para horários de medicação
- [ ] Exportação de relatórios (PDF, CSV)
- [ ] Interface gráfica (GUI) com tkinter ou PyQt
- [ ] API REST para integração com aplicativos móveis
- [ ] Histórico e estatísticas de aderência
- [ ] Suporte a múltiplos usuários (idosos/cuidadores)
