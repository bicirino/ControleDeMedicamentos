# Changelog

Todos às mudanças notáveis neste projeto terão documentação neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto respeita o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2025-04-22

### ✨ Adicionado

- **Interface Web moderna e responsiva** com HTML5, CSS3 e JavaScript vanilla
- **Design profissional** com sistema de cores consistente (60-30-10 rule, Azul Profundo)
- **Modo Claro/Escuro** com detecção automática de preferências do sistema
- **4 abas principais:**
  - 📆 **Hoje**: Visualização de medicamentos do dia com status
  - 📝 **Todos**: Lista completa de medicamentos cadastrados
  - ✨ **Novo**: Formulário para adicionar novos medicamentos
  - 🔍 **Consultar**: Busca inteligente com IA (Groq AI)
- **Layout totalmente responsivo** (Desktop, Tablet, Mobile)
- **Acessibilidade melhorada** com fontes legíveis e contraste apropriado
- **Integração com Groq AI** para consultas sobre medicamentos
- **Backend Flask** com 7 endpoints REST

### 🔄 Melhorias

- Interface gráfica substitui completamente a CLI
- Experiência de usuário otimizada para idosos
- Navegação intuitiva e clara
- Dados persistem automaticamente
- Sem necessidade de conhecimento técnico

### 🚀 Removido

- Interface CLI (main.py)
- Documentação relacionada a terminal/console
- Menu interativo em linha de comando

---

## [1.0.0] - 2025-04-10

### ✨ Adicionado (Versão Inicial)

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
- **Integração com Groq AI** para informações sobre medicamentos
- **Documentação completa** com README, instrções de instalação e uso
- **Licença MIT** para uso livre

---

## [Não Lançado]

### Futuras Melhorias Planejadas

- [ ] Notificações/alarmes para horários de medicação
- [ ] Exportação de relatórios (PDF, CSV)
- [ ] Histórico e estatísticas de aderência
- [ ] Suporte a múltiplos usuários (idosos/cuidadores)
- [ ] Integração com servidor para sincronização entre dispositivos
- [ ] Aplicativo mobile nativo

