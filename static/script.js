/**
 * script.js
 * Lógica da interface gráfica de Controle de Medicamentos
 */

// ==============================
// INICIALIZAÇÃO
// ==============================

document.addEventListener('DOMContentLoaded', () => {
    inicializarAplicacao();
});

const DIA_LABELS = {
    todos: 'Todos os dias',
    segunda: 'Segunda-feira',
    terca: 'Terça-feira',
    quarta: 'Quarta-feira',
    quinta: 'Quinta-feira',
    sexta: 'Sexta-feira',
    sabado: 'Sábado',
    domingo: 'Domingo'
};

// ==============================
// STORAGE LOCAL (localStorage)
// ==============================

const StorageManager = {
    // Chaves do localStorage
    MEDS_KEY: 'medicamentos_lista',
    TOMADOS_KEY: 'registros_tomados',
    VERSION_KEY: 'storage_version',
    STORAGE_VERSION: 1,

    /**
     * Inicializa o storage se não existir
     */
    inicializar() {
        if (!localStorage.getItem(this.MEDS_KEY)) {
            localStorage.setItem(this.MEDS_KEY, JSON.stringify([]));
        }
        if (!localStorage.getItem(this.TOMADOS_KEY)) {
            localStorage.setItem(this.TOMADOS_KEY, JSON.stringify([]));
        }
        localStorage.setItem(this.VERSION_KEY, this.STORAGE_VERSION);
    },

    /**
     * Salva um novo medicamento no localStorage
     */
    adicionarMedicamento(medicamento) {
        const meds = JSON.parse(localStorage.getItem(this.MEDS_KEY) || '[]');
        const novoId = meds.length > 0 ? Math.max(...meds.map(m => m.id)) + 1 : 1;
        const novoMed = { ...medicamento, observacao: medicamento.observacao || '', id: novoId, ativo: 1 };
        meds.push(novoMed);
        localStorage.setItem(this.MEDS_KEY, JSON.stringify(meds));
        return novoMed;
    },

    /**
     * Carrega todos os medicamentos ativos do localStorage
     */
    carregarMedicamentos() {
        const meds = JSON.parse(localStorage.getItem(this.MEDS_KEY) || '[]');
        return meds.filter(m => m.ativo === 1);
    },

    /**
     * Atualiza um medicamento no localStorage
     */
    atualizarMedicamento(id, dados) {
        const meds = JSON.parse(localStorage.getItem(this.MEDS_KEY) || '[]');
        const index = meds.findIndex(m => m.id === id);
        if (index !== -1) {
            meds[index] = { ...meds[index], ...dados, observacao: dados.observacao || '' };
            localStorage.setItem(this.MEDS_KEY, JSON.stringify(meds));
            return meds[index];
        }
        return null;
    },

    /**
     * Remove (desativa) um medicamento
     */
    removerMedicamento(id) {
        const meds = JSON.parse(localStorage.getItem(this.MEDS_KEY) || '[]');
        const index = meds.findIndex(m => m.id === id);
        if (index !== -1) {
            meds[index].ativo = 0;
            localStorage.setItem(this.MEDS_KEY, JSON.stringify(meds));
            return true;
        }
        return false;
    },

    /**
     * Marca medicamento como tomado hoje
     */
    marcarTomado(medicamentoId) {
        const hoje = _data_hoje();
        const tomados = JSON.parse(localStorage.getItem(this.TOMADOS_KEY) || '[]');
        
        // Verifica se já foi marcado hoje (converte para número para garantir comparação)
        const jaExiste = tomados.some(t => Number(t.medicamento_id) === Number(medicamentoId) && t.data_tomado === hoje);
        if (jaExiste) return false;
        
        tomados.push({ medicamento_id: Number(medicamentoId), data_tomado: hoje });
        localStorage.setItem(this.TOMADOS_KEY, JSON.stringify(tomados));
        return true;
    },

    /**
     * Desmarcar medicamento como tomado
     */
    desmarcarTomado(medicamentoId) {
        const hoje = _data_hoje();
        const tomados = JSON.parse(localStorage.getItem(this.TOMADOS_KEY) || '[]');
        const novosTomados = tomados.filter(t => !(Number(t.medicamento_id) === Number(medicamentoId) && t.data_tomado === hoje));
        localStorage.setItem(this.TOMADOS_KEY, JSON.stringify(novosTomados));
        return true;
    },

    /**
     * Verifica se medicamento foi tomado hoje
     */
    foiTomadoHoje(medicamentoId) {
        const hoje = _data_hoje();
        const tomados = JSON.parse(localStorage.getItem(this.TOMADOS_KEY) || '[]');
        return tomados.some(t => Number(t.medicamento_id) === Number(medicamentoId) && t.data_tomado === hoje);
    }
};

function inicializarAplicacao() {
    StorageManager.inicializar();
    configurarTema();
    configurarNavigacao();
    configurarFormularios();
    configurarModais();
    configurarDiaPadraoCadastro();
    atualizarDataHoje();
    carregarMedicamentosDoDay();
}

// ==============================
// TEMA CLARO/ESCURO
// ==============================

function configurarTema() {
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    if (!themeToggle) {
        return;
    }
    
    // Verificar preferência salva no localStorage
    const savedTheme = localStorage.getItem('theme');
    let isDarkMode = false;
    
    if (savedTheme) {
        // Usar preferência salva
        isDarkMode = savedTheme === 'dark';
    } else {
        // Usar preferência do sistema
        isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    
    // Aplicar tema inicial
    aplicarTema(isDarkMode);
    
    // Listener para o botão de toggle
    themeToggle.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        aplicarTema(newTheme === 'dark');
    });
    
    // Listener para mudanças de preferência do sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // Só aplicar se não houver preferência salva
        if (!localStorage.getItem('theme')) {
            aplicarTema(e.matches);
        }
    });
}

function aplicarTema(isDarkMode) {
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    
    if (isDarkMode) {
        htmlElement.setAttribute('data-theme', 'dark');
        if (themeToggle) {
            themeToggle.setAttribute('aria-label', 'Alternar para modo claro');
            themeToggle.setAttribute('title', 'Ativar tema claro');
            themeToggle.setAttribute('aria-pressed', 'true');
        }
    } else {
        htmlElement.setAttribute('data-theme', 'light');
        if (themeToggle) {
            themeToggle.setAttribute('aria-label', 'Alternar para modo escuro');
            themeToggle.setAttribute('title', 'Ativar tema escuro');
            themeToggle.setAttribute('aria-pressed', 'false');
        }
    }
}

function configurarNavigacao() {
    const navBtns = document.querySelectorAll('.nav-btn');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            mudarAba(tabName);
        });
    });
}

function mudarAba(tabName) {
    // Remover class active de todas as abas e botões
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
    });

    // Adicionar class active à aba e botão selecionado
    const tabContent = document.getElementById(`tab-${tabName}`);
    if (tabContent) {
        tabContent.classList.add('active');
    }

    const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.setAttribute('aria-selected', 'true');
    }

    // Carregar dados da aba se necessário
    if (tabName === 'todos') {
        carregarMedicamentosTodos();
    } else if (tabName === 'dia') {
        carregarMedicamentosDoDay();
    }
}

// ==============================
// ATUALIZAÇÃO DE DATA
// ==============================

function atualizarDataHoje() {
    const dataHoje = document.getElementById('dataHoje');
    const hoje = new Date();
    const opcoes = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dataFormatada = hoje.toLocaleDateString('pt-BR', opcoes);
    dataHoje.textContent = ` ${dataFormatada}`;
}

// ==============================
// CARREGAMENTO DE MEDICAMENTOS
// ==============================

async function carregarMedicamentosDoDay() {
    const container = document.getElementById('medicamentosDiaContainer');
    const loading = document.getElementById('loadingDia');
    const noDados = document.getElementById('noDadosDia');

    loading.style.display = 'block';
    container.innerHTML = '';
    noDados.style.display = 'none';

    try {
        // Carregar do localStorage (dados locais)
        const medicamentos = StorageManager.carregarMedicamentos();
        const hoje = _data_hoje();
        const diaSemanaHoje = _dia_semana_hoje();

        // Filtrar medicamentos do dia (todos + dia da semana)
        const medicamentosHoje = medicamentos.filter(med => 
            med.dia === 'todos' || med.dia === diaSemanaHoje
        );

        loading.style.display = 'none';

        if (medicamentosHoje.length === 0) {
            noDados.style.display = 'block';
            return;
        }

        const grupos = {
            manha: [],
            tarde: [],
            noite: []
        };

        medicamentosHoje.forEach(med => {
            const periodo = classificarPeriodoPorHorario(med.horario);
            // Verificar se foi tomado hoje
            const tomado = StorageManager.foiTomadoHoje(med.id);
            grupos[periodo].push({ ...med, tomado });
        });

        const secoes = [
            { chave: 'manha', titulo: '☀️ Manhã' },
            { chave: 'tarde', titulo: '🌤️ Tarde' },
            { chave: 'noite', titulo: '🌙 Noite' },
        ];

        secoes.forEach(secao => {
            if (grupos[secao.chave].length === 0) {
                return;
            }

            const wrapper = document.createElement('section');
            wrapper.className = 'periodo-secao';

            const titulo = document.createElement('h3');
            titulo.className = 'periodo-titulo';
            titulo.textContent = secao.titulo;

            const grid = document.createElement('div');
            grid.className = 'medicamentos-grid periodo-grid';

            grupos[secao.chave].forEach(med => {
                const card = criarCardMedicamento(med);
                grid.appendChild(card);
            });

            wrapper.appendChild(titulo);
            wrapper.appendChild(grid);
            container.appendChild(wrapper);
        });
    } catch (erro) {
        loading.style.display = 'none';
        mostrarAlerta('Erro ao conectar com o servidor', 'error');
        console.error('Erro:', erro);
    }
}

function obterMinutosAgora() {
    const agora = new Date();
    return (agora.getHours() * 60) + agora.getMinutes();
}

function converterHorarioParaMinutos(horario) {
    const [hora, minuto] = String(horario || '').split(':').map((parte) => Number(parte));
    if (!Number.isInteger(hora) || !Number.isInteger(minuto)) {
        return null;
    }
    return (hora * 60) + minuto;
}

function classificarPeriodoPorHorario(horario) {
    const hora = parseInt(String(horario || '').split(':')[0], 10);

    if (!Number.isInteger(hora)) {
        return 'manha';
    }

    if (hora < 12) {
        return 'manha';
    }

    if (hora < 18) {
        return 'tarde';
    }

    return 'noite';
}

async function carregarMedicamentosTodos() {
    const container = document.getElementById('medicamentosTodosContainer');
    const loading = document.getElementById('loadingTodos');
    const noDados = document.getElementById('noDadosTodos');

    loading.style.display = 'block';
    container.innerHTML = '';
    noDados.style.display = 'none';

    try {
        // Carregar do localStorage
        const medicamentos = StorageManager.carregarMedicamentos();

        loading.style.display = 'none';

        if (medicamentos.length === 0) {
            noDados.style.display = 'block';
            return;
        }

        const ordernarPorDia = (med) => {
            const diasOrd = ['todos', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'];
            return diasOrd.indexOf(med.dia);
        };

        medicamentos.sort((a, b) => {
            const ordA = ordernarPorDia(a);
            const ordB = ordernarPorDia(b);
            if (ordA !== ordB) return ordA - ordB;
            return a.horario.localeCompare(b.horario);
        });

        const tabela = criarTabelaMedicamentos(medicamentos);
        container.appendChild(tabela);
    } catch (erro) {
        loading.style.display = 'none';
        mostrarAlerta('Erro ao conectar com o servidor', 'error');
        console.error('Erro:', erro);
    }
}

// ==============================
// CRIAR ELEMENTOS
// ==============================

function criarCardMedicamento(med) {
    const card = document.createElement('div');
    const atrasado = !med.tomado && estaHorarioAtrasado(med.horario);
    card.className = `medicamento-card ${med.tomado ? 'tomado' : ''} ${atrasado ? 'atrasado' : ''}`;

    const statusClasse = med.tomado ? 'tomado' : (atrasado ? 'atrasado' : 'pendente');
    const statusTexto = med.tomado ? '✓ Tomado' : (atrasado ? '⚠ Atrasado' : '⏳ Pendente');

    const header = document.createElement('div');
    header.className = 'medicamento-header';

    const nome = document.createElement('h3');
    nome.className = 'medicamento-nome';
    nome.textContent = med.nome;
    header.appendChild(nome);

    const dia = document.createElement('div');
    dia.className = 'medicamento-dia';
    dia.textContent = `📆 ${formatarDiaMedicamento(med.dia)}`;

    const dosagem = document.createElement('div');
    dosagem.className = 'medicamento-dosagem';
    dosagem.innerHTML = `<strong>Dosagem:</strong> ${escaparHTML(med.dosagem)}`;

    const horario = document.createElement('div');
    horario.className = 'medicamento-horario';
    horario.textContent = `🕐 ${med.horario}`;

    const observacao = document.createElement('div');
    observacao.className = 'medicamento-observacao';
    observacao.innerHTML = `<strong>Obs:</strong> ${escaparHTML(med.observacao || 'Sem observação')}`;

    const status = document.createElement('div');
    status.className = `medicamento-status ${statusClasse}`;
    status.textContent = statusTexto;

    const actions = document.createElement('div');
    actions.className = 'medicamento-actions';

    const actionButton = med.tomado
        ? criarBotaoAcaoMedicamento('btn-acao btn btn-secondary btn-desfazer-tomado', 'Desfazer', med)
        : criarBotaoAcaoMedicamento('btn-acao btn btn-success btn-marcar-tomado', '✓ Marcar como Tomado', med);
    actions.appendChild(actionButton);

    card.appendChild(header);
    card.appendChild(dia);
    card.appendChild(dosagem);
    card.appendChild(horario);
    card.appendChild(observacao);
    card.appendChild(status);
    card.appendChild(actions);

    return card;
}

function criarBotaoAcaoMedicamento(classes, texto, med) {
    const btn = document.createElement('button');
    btn.className = classes;
    btn.dataset.medId = String(med.id);
    btn.dataset.medNome = med.nome;
    btn.textContent = texto;
    return btn;
}

function estaHorarioAtrasado(horario) {
    const minutosHorario = converterHorarioParaMinutos(horario);
    if (minutosHorario === null) {
        return false;
    }

    return minutosHorario < obterMinutosAgora();
}

function criarTabelaMedicamentos(medicamentos) {
    const tabela = document.createElement('table');
    tabela.setAttribute('role', 'table');

    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Medicamento</th>
            <th>Dia</th>
            <th>Dosagem</th>
            <th>Horário</th>
            <th>Observação</th>
            <th>Status</th>
            <th>Ações</th>
        </tr>
    `;
    tabela.appendChild(thead);

    const tbody = document.createElement('tbody');

    medicamentos.forEach(med => {
        const tr = document.createElement('tr');
        tr.className = !med.ativo ? 'inativo' : '';

        const statusTexto = med.ativo ? 'Ativo' : 'Inativo';
        const statusClasse = med.ativo ? 'status-ativo' : 'status-inativo';

        const tdNome = document.createElement('td');
        tdNome.textContent = med.nome;

        const tdDia = document.createElement('td');
        tdDia.textContent = formatarDiaMedicamento(med.dia);

        const tdDosagem = document.createElement('td');
        tdDosagem.textContent = med.dosagem;

        const tdHorario = document.createElement('td');
        tdHorario.textContent = med.horario;

        const tdObservacao = document.createElement('td');
        tdObservacao.textContent = med.observacao || 'Sem observação';

        const tdStatus = document.createElement('td');
        tdStatus.className = statusClasse;
        tdStatus.textContent = statusTexto;

        const tdAcoes = document.createElement('td');
        tdAcoes.className = 'acoes-tabela';

        const btnEditar = document.createElement('button');
        btnEditar.className = 'btn btn-secondary btn-editar-med';
        btnEditar.dataset.medId = String(med.id);
        btnEditar.dataset.medNome = med.nome;
        btnEditar.dataset.medDosagem = med.dosagem;
        btnEditar.dataset.medHorario = med.horario;
        btnEditar.dataset.medObservacao = med.observacao || '';
        btnEditar.dataset.medDia = String(med.dia || 'todos');
        btnEditar.textContent = 'Editar';

        const btnRemover = document.createElement('button');
        btnRemover.className = 'btn btn-danger btn-remover-med';
        btnRemover.dataset.medId = String(med.id);
        btnRemover.dataset.medNome = med.nome;
        btnRemover.textContent = 'Remover';

        tdAcoes.appendChild(btnEditar);
        tdAcoes.appendChild(btnRemover);

        tr.appendChild(tdNome);
        tr.appendChild(tdDia);
        tr.appendChild(tdDosagem);
        tr.appendChild(tdHorario);
        tr.appendChild(tdObservacao);
        tr.appendChild(tdStatus);
        tr.appendChild(tdAcoes);

        tbody.appendChild(tr);
    });

    tabela.appendChild(tbody);
    return tabela;
}

// ==============================
// FORMULÁRIOS
// ==============================

function configurarFormularios() {
    const formCadastrar = document.getElementById('formCadastrar');
    const formConsultar = document.getElementById('formConsultar');

    if (formCadastrar) {
        formCadastrar.addEventListener('submit', async (e) => {
            e.preventDefault();
            await submeterFormularioCadastro();
        });
    }

    if (formConsultar) {
        formConsultar.addEventListener('submit', async (e) => {
            e.preventDefault();
            await submeterFormularioConsulta();
        });
    }

    if (formCadastrar) {
        formCadastrar.addEventListener('reset', () => {
            setTimeout(configurarDiaPadraoCadastro, 0);
        });
    }
}

function configurarDiaPadraoCadastro() {
    const inputDia = document.getElementById('inputDia');
    if (!inputDia) {
        return;
    }

    inputDia.value = obterDiaSemanaAtualValor();
}

function obterDiaSemanaAtualValor() {
    const dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
    return dias[new Date().getDay()];
}

async function submeterFormularioCadastro() {
    const nome = document.getElementById('inputNome').value.trim();
    const dosagem = document.getElementById('inputDosagem').value.trim();
    const horario = document.getElementById('inputHorario').value.trim();
    const observacao = document.getElementById('inputObservacao').value.trim();
    const dia = document.getElementById('inputDia').value;
    const mensagem = document.getElementById('formMessage');

    if (!nome || !dosagem || !horario || !dia) {
        mensagem.className = 'form-message error';
        mensagem.textContent = '⚠️ Todos os campos são obrigatórios!';
        return;
    }

    try {
        // Salvar no localStorage (storage local)
        const novoMed = StorageManager.adicionarMedicamento({
            nome: nome,
            dosagem: dosagem,
            horario: horario,
            observacao: observacao,
            dia: dia
        });

        if (novoMed) {
            mensagem.className = 'form-message success';
            mensagem.textContent = `✅ Medicamento '${nome}' cadastrado com sucesso!`;

            // Limpar formulário
            document.getElementById('formCadastrar').reset();

            // Recarregar medicamentos
            carregarMedicamentosDoDay();
            carregarMedicamentosTodos();

            // Limpar mensagem após 3 segundos
            setTimeout(() => {
                mensagem.textContent = '';
                mensagem.className = 'form-message';
            }, 3000);
        } else {
            mensagem.className = 'form-message error';
            mensagem.textContent = '❌ Erro ao cadastrar medicamento';
        }
    } catch (erro) {
        mensagem.className = 'form-message error';
        mensagem.textContent = '❌ Erro ao cadastrar medicamento';
        console.error('Erro:', erro);
    }
}

function formatarDiaMedicamento(dia) {
    const chave = String(dia || 'todos').toLowerCase();
    return DIA_LABELS[chave] || 'Todos os dias';
}

async function submeterFormularioConsulta() {
    const nome = document.getElementById('inputConsultaNome').value.trim();
    const loading = document.getElementById('loadingConsulta');
    const resultado = document.getElementById('consultaResultado');
    const mensagem = document.getElementById('consultaMessage');

    if (!nome) {
        mensagem.className = 'form-message error';
        mensagem.textContent = '⚠️ Informe o nome do medicamento!';
        return;
    }

    loading.style.display = 'block';
    resultado.style.display = 'none';
    mensagem.textContent = '';
    mensagem.className = 'form-message';

    try {
        const response = await fetch(`/api/medicamentos/${encodeURIComponent(nome)}/consultar`);
        const dados = await response.json();

        loading.style.display = 'none';

        if (dados.sucesso) {
            document.getElementById('consultaMedicamento').textContent = `💊 ${dados.medicamento}`;
            document.getElementById('consultaInfo').innerHTML = dados.informacoes;
            resultado.style.display = 'block';
        } else {
            mensagem.className = 'form-message error';
            mensagem.textContent = `❌ ${dados.erro}`;
        }
    } catch (erro) {
        loading.style.display = 'none';
        mensagem.className = 'form-message error';
        mensagem.textContent = '❌ Erro ao consultar medicamento';
        console.error('Erro:', erro);
    }
}

// ==============================
// MODAIS
// ==============================

function configurarModais() {
    const modalMarcado = document.getElementById('modalMarcado');
    const modalRemover = document.getElementById('modalRemover');
    const modalEditar = document.getElementById('modalEditar');

    const btnCancelarMarcado = document.getElementById('btnCancelar');
    const btnCancelarRemover = document.getElementById('btnCancelarRemover');
    const btnCancelarEditar = document.getElementById('btnCancelarEditar');
    const formEditar = document.getElementById('formEditarMedicamento');

    if (btnCancelarMarcado) {
        btnCancelarMarcado.addEventListener('click', () => {
            modalMarcado.close();
        });
    }

    if (btnCancelarRemover) {
        btnCancelarRemover.addEventListener('click', () => {
            modalRemover.close();
        });
    }

    if (btnCancelarEditar && modalEditar) {
        btnCancelarEditar.addEventListener('click', () => {
            modalEditar.close();
        });
    }

    if (formEditar && modalEditar) {
        formEditar.addEventListener('submit', async (e) => {
            e.preventDefault();
            const medId = document.getElementById('editarMedId').value;
            const nome = document.getElementById('editarNome').value.trim();
            const dosagem = document.getElementById('editarDosagem').value.trim();
            const horario = document.getElementById('editarHorario').value;
            const observacao = document.getElementById('editarObservacao').value.trim();
            const dia = document.getElementById('editarDia').value;

            await atualizarMedicamento(medId, { nome, dosagem, horario, observacao, dia });
            modalEditar.close();
        });
    }

    // Fechar modal ao clicar fora
    if (modalMarcado) {
        modalMarcado.addEventListener('click', (e) => {
            if (e.target === modalMarcado) {
                modalMarcado.close();
            }
        });
    }

    if (modalRemover) {
        modalRemover.addEventListener('click', (e) => {
            if (e.target === modalRemover) {
                modalRemover.close();
            }
        });
    }

    if (modalEditar) {
        modalEditar.addEventListener('click', (e) => {
            if (e.target === modalEditar) {
                modalEditar.close();
            }
        });
    }

    // Listeners para botões de ação (evento delegado)
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-marcar-tomado')) {
            const medId = e.target.dataset.medId;
            const medNome = e.target.dataset.medNome;
            abrirModalTomado(medId, medNome, false);
        }

        if (e.target.classList.contains('btn-desfazer-tomado')) {
            const medId = e.target.dataset.medId;
            const medNome = e.target.dataset.medNome;
            abrirModalTomado(medId, medNome, true);
        }

        if (e.target.classList.contains('btn-remover-med')) {
            const medId = e.target.dataset.medId;
            const medNome = e.target.dataset.medNome;
            abrirModalRemover(medId, medNome);
        }

        if (e.target.classList.contains('btn-editar-med')) {
            abrirModalEditar({
                id: e.target.dataset.medId,
                nome: e.target.dataset.medNome,
                dosagem: e.target.dataset.medDosagem,
                horario: e.target.dataset.medHorario,
                observacao: e.target.dataset.medObservacao || '',
                dia: e.target.dataset.medDia || 'todos'
            });
        }
    });
}

function abrirModalEditar(med) {
    const modal = document.getElementById('modalEditar');
    document.getElementById('editarMedId').value = med.id;
    document.getElementById('editarNome').value = med.nome;
    document.getElementById('editarDosagem').value = med.dosagem;
    document.getElementById('editarHorario').value = med.horario;
    document.getElementById('editarObservacao').value = med.observacao || '';
    document.getElementById('editarDia').value = String(med.dia || 'todos').toLowerCase();
    modal.showModal();
}

function abrirModalTomado(medId, nome, desfazer = false) {
    const modal = document.getElementById('modalMarcado');
    const mensagem = document.getElementById('modalMensagem');
    const btnConfirmar = document.getElementById('btnConfirmar');
    const titulo = document.getElementById('modalTitulo');

    if (desfazer) {
        if (titulo) titulo.textContent = 'Desfazer Marcação';
        mensagem.textContent = `Você deseja desmarcar "${nome}" como tomado?`;
        btnConfirmar.textContent = 'Desfazer';
        btnConfirmar.className = 'btn btn-secondary';
    } else {
        if (titulo) titulo.textContent = 'Confirmar Ação';
        mensagem.textContent = `Você deseja marcar "${nome}" como tomado?`;
        btnConfirmar.textContent = '✅ Confirmar';
        btnConfirmar.className = 'btn btn-primary';
    }

    btnConfirmar.onclick = async () => {
        if (desfazer) {
            await desmarcarMedicamentoComoTomado(medId);
        } else {
            await marcarMedicamentoComoTomado(medId);
        }
        modal.close();
    };

    modal.showModal();
}

function abrirModalRemover(medId, nome) {
    const modal = document.getElementById('modalRemover');
    const mensagem = document.getElementById('modalRemoverMensagem');
    const btnConfirmar = document.getElementById('btnConfirmarRemover');

    mensagem.textContent = `Você deseja remover "${nome}"? Esta ação não pode ser desfeita.`;

    btnConfirmar.onclick = async () => {
        await removerMedicamento(medId, nome);
        modal.close();
    };

    modal.showModal();
}

// ==============================
// AÇÕES COM MEDICAMENTOS
// ==============================

async function marcarMedicamentoComoTomado(medId) {
    try {
        // Marcar no localStorage
        const sucesso = StorageManager.marcarTomado(medId);

        if (!sucesso) {
            mostrarAlerta('❌ Medicamento já foi marcado como tomado hoje', 'error');
            return;
        }

        const med = StorageManager.carregarMedicamentos().find(m => m.id === medId);
        if (med) {
            mostrarAlerta(`✅ '${med.nome}' marcado como tomado!`, 'success');
        }
        carregarMedicamentosDoDay();
    } catch (erro) {
        mostrarAlerta('❌ Erro ao marcar medicamento', 'error');
        console.error('Erro:', erro);
    }
}

async function desmarcarMedicamentoComoTomado(medId) {
    try {
        // Desmarcar no localStorage
        StorageManager.desmarcarTomado(medId);

        const med = StorageManager.carregarMedicamentos().find(m => m.id === medId);
        if (med) {
            mostrarAlerta(`✅ Marcação de '${med.nome}' desfeita!`, 'success');
        }
        carregarMedicamentosDoDay();
    } catch (erro) {
        mostrarAlerta('❌ Erro ao desfazer marcação do medicamento', 'error');
        console.error('Erro:', erro);
    }
}

async function removerMedicamento(medId, nome) {
    try {
        // Remover do localStorage
        const sucesso = StorageManager.removerMedicamento(medId);

        if (sucesso) {
            mostrarAlerta(`✅ Medicamento '${nome}' removido!`, 'success');
            carregarMedicamentosDoDay();
            carregarMedicamentosTodos();
        } else {
            mostrarAlerta('❌ Erro ao remover medicamento', 'error');
        }
    } catch (erro) {
        mostrarAlerta('❌ Erro ao remover medicamento', 'error');
        console.error('Erro:', erro);
    }
}

async function atualizarMedicamento(medId, payload) {
    try {
        // Atualizar no localStorage
        const med = StorageManager.atualizarMedicamento(medId, payload);

        if (med) {
            mostrarAlerta(`✅ Medicamento atualizado com sucesso!`, 'success');
            carregarMedicamentosDoDay();
            carregarMedicamentosTodos();
        } else {
            mostrarAlerta('❌ Medicamento não encontrado', 'error');
        }
    } catch (erro) {
        mostrarAlerta('❌ Erro ao atualizar medicamento', 'error');
        console.error('Erro:', erro);
    }
}

// ==============================
// ALERTAS
// ==============================

function mostrarAlerta(mensagem, tipo = 'info') {
    const container = document.getElementById('alertContainer');

    const alert = document.createElement('div');
    alert.className = `alert ${tipo}`;
    alert.setAttribute('role', 'alert');
    alert.textContent = mensagem;

    container.appendChild(alert);

    // Remover alerta após 4 segundos
    setTimeout(() => {
        alert.classList.add('removing');
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, 4000);
}

// ==============================
// UTILITÁRIOS
// ==============================

/**
 * Retorna a data atual no formato YYYY-MM-DD
 */
function _data_hoje() {
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = String(hoje.getMonth() + 1).padStart(2, '0');
    const dia = String(hoje.getDate()).padStart(2, '0');
    return `${ano}-${mes}-${dia}`;
}

/**
 * Retorna o dia da semana atual no formato interno
 * (segunda, terca, quarta, quinta, sexta, sabado, domingo)
 */
function _dia_semana_hoje() {
    const diasMapa = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
    return diasMapa[new Date().getDay()];
}

function escaparHTML(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

// Recarregar dados a cada 30 segundos (para manter atualizado em tempo real)
setInterval(() => {
    const tabAtiva = document.querySelector('.tab-content.active');
    if (tabAtiva && tabAtiva.id === 'tab-dia') {
        carregarMedicamentosDoDay();
    }
}, 30000);
