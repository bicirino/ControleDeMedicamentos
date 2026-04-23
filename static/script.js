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

function inicializarAplicacao() {
    configurarTema();
    configurarNavigacao();
    configurarFormularios();
    configurarModais();
    atualizarDataHoje();
    carregarMedicamentosDoDay();
}

// ==============================
// TEMA CLARO/ESCURO
// ==============================

function configurarTema() {
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
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
        themeToggle.textContent = '☀️';
        themeToggle.setAttribute('aria-label', 'Alternar para modo claro');
    } else {
        htmlElement.setAttribute('data-theme', 'light');
        themeToggle.textContent = '🌙';
        themeToggle.setAttribute('aria-label', 'Alternar para modo escuro');
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

        dados.medicamentos.forEach(med => {
            const card = criarCardMedicamento(med);
            container.appendChild(card);
        });
    } catch (erro) {
        loading.style.display = 'none';
        mostrarAlerta('Erro ao conectar com o servidor', 'error');
        console.error('Erro:', erro);
    }
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
    card.className = `medicamento-card ${med.tomado ? 'tomado' : ''}`;

    const statusTexto = med.tomado ? '✅ Tomado' : '⏳ Pendente';
    const statusClasse = med.tomado ? 'tomado' : 'pendente';

    let botao = '';
    if (!med.tomado) {
        botao = `
            <button class="btn-acao btn btn-success" onclick="abrirModalMarcado(${med.id}, '${med.nome}')">
                ✅ Marcar como Tomado
            </button>
        `;
    }

    card.innerHTML = `
        <div class="medicamento-header">
            <span class="medicamento-icon">💊</span>
            <h3 class="medicamento-nome">${escaparHTML(med.nome)}</h3>
        </div>
        <div class="medicamento-dosagem">💪 ${escaparHTML(med.dosagem)}</div>
        <div class="medicamento-horario">🕐 ${med.horario}</div>
        <div class="medicamento-status ${statusClasse}">${statusTexto}</div>
        <div class="medicamento-actions">
            ${botao}
            <button class="btn-acao btn btn-danger" onclick="abrirModalRemover(${med.id}, '${med.nome}')">
                 Remover
            </button>
        </div>
    `;

    return card;
}

function criarTabelaMedicamentos(medicamentos) {
    const tabela = document.createElement('table');
    tabela.setAttribute('role', 'table');

    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Medicamento</th>
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

        tr.innerHTML = `
            <td>${escaparHTML(med.nome)}</td>
            <td>${escaparHTML(med.dosagem)}</td>
            <td>${med.horario}</td>
            <td class="${statusClasse}">${statusTexto}</td>
            <td>
                <button class="btn btn-danger" onclick="abrirModalRemover(${med.id}, '${med.nome}')">
                     Remover
                </button>
            </td>
        `;

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
}

async function submeterFormularioCadastro() {
    const nome = document.getElementById('inputNome').value.trim();
    const dosagem = document.getElementById('inputDosagem').value.trim();
    const horario = document.getElementById('inputHorario').value.trim();
    const mensagem = document.getElementById('formMessage');

    if (!nome || !dosagem || !horario) {
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
                horario: horario
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
            document.getElementById('consultaInfo').textContent = dados.informacoes;
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

    const btnCancelarMarcado = document.getElementById('btnCancelar');
    const btnCancelarRemover = document.getElementById('btnCancelarRemover');

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
}

function abrirModalMarcado(medId, nome) {
    const modal = document.getElementById('modalMarcado');
    const mensagem = document.getElementById('modalMensagem');
    const btnConfirmar = document.getElementById('btnConfirmar');

    mensagem.textContent = `Você deseja marcar "${escaparHTML(nome)}" como tomado?`;

    btnConfirmar.onclick = async () => {
        await marcarMedicamentoComoTomado(medId, nome);
        modal.close();
    };

    modal.showModal();
}

function abrirModalRemover(medId, nome) {
    const modal = document.getElementById('modalRemover');
    const mensagem = document.getElementById('modalRemoverMensagem');
    const btnConfirmar = document.getElementById('btnConfirmarRemover');

    mensagem.textContent = `Você deseja remover "${escaparHTML(nome)}"? Esta ação não pode ser desfeita.`;

    btnConfirmar.onclick = async () => {
        await removerMedicamento(medId, nome);
        modal.close();
    };

    modal.showModal();
}

// ==============================
// AÇÕES COM MEDICAMENTOS
// ==============================

async function marcarMedicamentoComoTomado(medId, nome) {
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
