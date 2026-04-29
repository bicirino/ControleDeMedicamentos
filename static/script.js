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

function inicializarAplicacao() {
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
        const currentTheme = htmlElement.getAttribute('data-theme');
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
        const response = await fetch('/api/medicamentos/dia');
        const dados = await response.json();

        loading.style.display = 'none';

        if (!dados.sucesso) {
            mostrarAlerta('Erro ao carregar medicamentos', 'error');
            return;
        }

        if (dados.medicamentos.length === 0) {
            noDados.style.display = 'block';
            return;
        }

        const grupos = {
            manha: [],
            tarde: [],
            noite: []
        };

        dados.medicamentos.forEach(med => {
            const periodo = classificarPeriodoPorHorario(med.horario);
            grupos[periodo].push(med);
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
        const response = await fetch('/api/medicamentos/todos');
        const dados = await response.json();

        loading.style.display = 'none';

        if (!dados.sucesso) {
            mostrarAlerta('Erro ao carregar medicamentos', 'error');
            return;
        }

        if (dados.medicamentos.length === 0) {
            noDados.style.display = 'block';
            return;
        }

        const tabela = criarTabelaMedicamentos(dados.medicamentos);
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
    const dia = document.getElementById('inputDia').value;
    const mensagem = document.getElementById('formMessage');

    if (!nome || !dosagem || !horario || !dia) {
        mensagem.className = 'form-message error';
        mensagem.textContent = '⚠️ Todos os campos são obrigatórios!';
        return;
    }

    try {
        const response = await fetch('/api/medicamentos/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nome: nome,
                dosagem: dosagem,
                horario: horario,
                dia: dia
            })
        });

        const dados = await response.json();

        if (dados.sucesso) {
            mensagem.className = 'form-message success';
            mensagem.textContent = `✅ ${dados.mensagem}`;

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
            mensagem.textContent = `❌ ${dados.erro}`;
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
            const dia = document.getElementById('editarDia').value;

            await atualizarMedicamento(medId, { nome, dosagem, horario, dia });
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
        const response = await fetch(`/api/medicamentos/${medId}/marcar-tomado`, {
            method: 'POST'
        });

        const dados = await response.json();

        if (dados.sucesso) {
            mostrarAlerta(`✅ ${dados.mensagem}`, 'success');
            carregarMedicamentosDoDay();
        } else {
            mostrarAlerta(`❌ ${dados.erro}`, 'error');
        }
    } catch (erro) {
        mostrarAlerta('❌ Erro ao marcar medicamento', 'error');
        console.error('Erro:', erro);
    }
}

async function desmarcarMedicamentoComoTomado(medId) {
    try {
        const response = await fetch(`/api/medicamentos/${medId}/desmarcar-tomado`, {
            method: 'DELETE'
        });

        const dados = await response.json();

        if (dados.sucesso) {
            mostrarAlerta(`✅ ${dados.mensagem}`, 'success');
            carregarMedicamentosDoDay();
        } else {
            mostrarAlerta(`❌ ${dados.erro}`, 'error');
        }
    } catch (erro) {
        mostrarAlerta('❌ Erro ao desfazer marcação do medicamento', 'error');
        console.error('Erro:', erro);
    }
}

async function removerMedicamento(medId, nome) {
    try {
        const response = await fetch(`/api/medicamentos/${medId}/remover`, {
            method: 'DELETE'
        });

        const dados = await response.json();

        if (dados.sucesso) {
            mostrarAlerta(`✅ ${dados.mensagem}`, 'success');
            carregarMedicamentosDoDay();
            carregarMedicamentosTodos();
        } else {
            mostrarAlerta(`❌ ${dados.erro}`, 'error');
        }
    } catch (erro) {
        mostrarAlerta('❌ Erro ao remover medicamento', 'error');
        console.error('Erro:', erro);
    }
}

async function atualizarMedicamento(medId, payload) {
    try {
        const response = await fetch(`/api/medicamentos/${medId}/editar`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        const dados = await response.json();

        if (dados.sucesso) {
            mostrarAlerta(`✅ ${dados.mensagem}`, 'success');
            carregarMedicamentosDoDay();
            carregarMedicamentosTodos();
        } else {
            mostrarAlerta(`❌ ${dados.erro}`, 'error');
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
