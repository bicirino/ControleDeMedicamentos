"""
app.py
Aplicação Flask para interface web do Controle de Medicamentos.
Expõe endpoints REST que integram com a lógica de negócio existente.
"""

import os
import re
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_conexao, inicializar_banco
from medicamentos import (
    _data_hoje,
    _validar_horario,
)
from api_integration import buscar_medicamento_groq, APIError

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

# Inicializar banco ao iniciar a aplicação
inicializar_banco()

DIAS_VALIDOS = {
    "todos",
    "segunda",
    "terca",
    "quarta",
    "quinta",
    "sexta",
    "sabado",
    "domingo",
}

MAPA_DIA_SEMANA = {
    0: "segunda",
    1: "terca",
    2: "quarta",
    3: "quinta",
    4: "sexta",
    5: "sabado",
    6: "domingo",
}


def _dia_semana_hoje() -> str:
    """Retorna o dia da semana atual no formato interno."""
    return MAPA_DIA_SEMANA[datetime.now().weekday()]


def _normalizar_dia(dia: str) -> str:
    """Normaliza o dia recebido para o formato persistido no banco."""
    return str(dia).strip().lower()


def formatar_resposta_medicamento(texto: str) -> str:
    """
    Formata a resposta do medicamento removendo asteríscos e numeração,
    convertendo para bullet points e deixando títulos em negrito.

    Args:
        texto: Texto com formatação de asteríscos e numeração

    Returns:
        Texto formatado com bullet points e títulos em HTML bold
    """
    # Remove asteríscos de formatação
    texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto)
    texto = re.sub(r'\*([^*]+)\*', r'\1', texto)

    # Substitui numeração por bullet points
    texto = re.sub(r'^\d+\.\s', '• ', texto, flags=re.MULTILINE)

    # Remove asteríscos de bullet points do início de linhas
    texto = re.sub(r'^\*\s', '• ', texto, flags=re.MULTILINE)

    # Deixa títulos em negrito (padrão: "Título": ou Título:)
    # Primeiro padrão: "Título":
    texto = re.sub(r'"([^"]+)":', r'<strong>\1</strong>:', texto)
    # Segundo padrão: linha que começa com título (sem aspas)
    regex = r'^• ([A-Z][^:]*?):\s'
    replace = r'• <strong>\1</strong>: '
    texto = re.sub(regex, replace, texto, flags=re.MULTILINE)

    return texto.strip()


# ==============================
# AUTENTICAÇÃO
# ==============================

def login_required(f):
    """Decorador para proteger rotas que requerem autenticação."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            return jsonify({
                "sucesso": False,
                "erro": "Não autenticado",
                "requer_login": True
            }), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route("/api/auth/registro", methods=["POST"])
def registrar():
    """Registra um novo usuário."""
    try:
        dados = request.get_json(silent=True)
        if dados is None:
            return jsonify({
                "sucesso": False,
                "erro": "JSON inválido"
            }), 400

        email = dados.get("email", "").strip().lower()
        nome = dados.get("nome", "").strip()
        senha = dados.get("senha", "").strip()

        if not email:
            return jsonify({
                "sucesso": False,
                "erro": "Email é obrigatório"
            }), 400

        if not nome:
            return jsonify({
                "sucesso": False,
                "erro": "Nome é obrigatório"
            }), 400

        if not senha or len(senha) < 6:
            return jsonify({
                "sucesso": False,
                "erro": "Senha deve ter no mínimo 6 caracteres"
            }), 400

        if "@" not in email or "." not in email:
            return jsonify({
                "sucesso": False,
                "erro": "Email inválido"
            }), 400

        conexao = get_conexao()
        cursor = conexao.cursor()

        # Verificar se usuário já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({
                "sucesso": False,
                "erro": "Este email já está cadastrado"
            }), 400

        # Inserir novo usuário
        senha_hash = generate_password_hash(senha)
        cursor.execute(
            "INSERT INTO usuarios (email, nome, senha_hash, criado_em) "
            "VALUES (?, ?, ?, ?)",
            (email, nome, senha_hash, datetime.now().isoformat()),
        )
        conexao.commit()
        novo_id = cursor.lastrowid
        conexao.close()

        # Criar sessão automaticamente (persistente por 30 dias)
        session.permanent = True
        session["usuario_id"] = novo_id
        session["email"] = email
        session["nome"] = nome

        return jsonify({
            "sucesso": True,
            "mensagem": f"Bem-vindo, {nome}!",
            "usuario": {
                "id": novo_id,
                "email": email,
                "nome": nome
            }
        })
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500


@app.route("/api/auth/login", methods=["POST"])
def login():
    """Realiza o login do usuário."""
    try:
        dados = request.get_json(silent=True)
        if dados is None:
            return jsonify({
                "sucesso": False,
                "erro": "JSON inválido"
            }), 400

        email = dados.get("email", "").strip().lower()
        senha = dados.get("senha", "").strip()
        lembrar_me = bool(dados.get("lembrar_me", False))

        if not email or not senha:
            return jsonify({
                "sucesso": False,
                "erro": "Email e senha são obrigatórios"
            }), 400

        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id, nome, senha_hash FROM usuarios WHERE email = ?",
            (email,),
        )
        usuario = cursor.fetchone()
        conexao.close()

        if not usuario or not check_password_hash(
            usuario["senha_hash"],
            senha,
        ):
            return jsonify({
                "sucesso": False,
                "erro": "Email ou senha inválidos"
            }), 401

        # Criar sessão
        session.permanent = lembrar_me
        session["usuario_id"] = usuario["id"]
        session["email"] = email
        session["nome"] = usuario["nome"]

        return jsonify({
            "sucesso": True,
            "mensagem": f"Bem-vindo, {usuario['nome']}!",
            "usuario": {
                "id": usuario["id"],
                "email": email,
                "nome": usuario["nome"]
            }
        })
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500


@app.route("/api/auth/me", methods=["GET"])
@login_required
def get_usuario_logado():
    """Retorna informações do usuário logado."""
    return jsonify({
        "sucesso": True,
        "usuario": {
            "id": session.get("usuario_id"),
            "email": session.get("email"),
            "nome": session.get("nome")
        }
    })


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Realiza o logout do usuário."""
    session.clear()
    return jsonify({
        "sucesso": True,
        "mensagem": "Desconectado com sucesso"
    })


@app.route("/")
def index():
    """Renderiza a página principal."""
    if "usuario_id" not in session:
        return render_template("login.html")
    return render_template("index.html")


@app.route("/api/medicamentos/dia", methods=["GET"])
@login_required
def get_medicamentos_dia():
    """Retorna medicamentos do dia com status de tomado."""
    try:
        hoje = _data_hoje()
        dia_hoje = _dia_semana_hoje()
        usuario_id = session["usuario_id"]

        with get_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, dosagem, horario, dia, observacao "
                "FROM medicamentos WHERE usuario_id = ? "
                "AND ativo = 1 AND (dia = 'todos' OR dia = ?) "
                "ORDER BY horario",
                (usuario_id, dia_hoje),
            )
            medicamentos = cursor.fetchall()
            cursor.execute(
                "SELECT medicamento_id FROM registros_tomados "
                "WHERE data_tomado = ?",
                (hoje,),
            )
            ids_tomados = {row["medicamento_id"] for row in cursor.fetchall()}

        resultado = []
        for med in medicamentos:
            observacao = (
                med["observacao"]
                if "observacao" in med.keys()
                else ""
            )
            resultado.append({
                "id": med["id"],
                "nome": med["nome"],
                "dosagem": med["dosagem"],
                "horario": med["horario"],
                "dia": med["dia"],
                "observacao": observacao,
                "tomado": med["id"] in ids_tomados
            })

        return jsonify({
            "sucesso": True,
            "data": hoje,
            "medicamentos": resultado
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/todos", methods=["GET"])
@login_required
def get_todos_medicamentos():
    """Retorna todos os medicamentos cadastrados (apenas ativos)."""
    try:
        usuario_id = session["usuario_id"]
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id, nome, dosagem, horario, dia, observacao, ativo "
            "FROM medicamentos WHERE usuario_id = ? "
            "AND ativo = 1 "
            "ORDER BY "
            "CASE dia "
            "WHEN 'todos' THEN 0 "
            "WHEN 'segunda' THEN 1 "
            "WHEN 'terca' THEN 2 "
            "WHEN 'quarta' THEN 3 "
            "WHEN 'quinta' THEN 4 "
            "WHEN 'sexta' THEN 5 "
            "WHEN 'sabado' THEN 6 "
            "WHEN 'domingo' THEN 7 "
            "ELSE 8 END, horario",
            (usuario_id,)
        )
        medicamentos = cursor.fetchall()

        resultado = []
        for med in medicamentos:
            observacao = (
                med["observacao"]
                if "observacao" in med.keys()
                else ""
            )
            resultado.append({
                "id": med["id"],
                "nome": med["nome"],
                "dosagem": med["dosagem"],
                "horario": med["horario"],
                "dia": med["dia"],
                "observacao": observacao,
                "ativo": med["ativo"] == 1
            })

        return jsonify({
            "sucesso": True,
            "medicamentos": resultado
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/cadastrar", methods=["POST"])
@login_required
def cadastrar_medicamento():
    """Cadastra um novo medicamento."""
    try:
        usuario_id = session["usuario_id"]
        dados = request.get_json(silent=True)
        if dados is None:
            return jsonify({
                "sucesso": False,
                "erro": "JSON inválido ou ausente no corpo da requisição"
            }), 400

        nome = dados.get("nome", "").strip()
        if not nome:
            erro_msg = "Nome não pode ser vazio"
            return jsonify({"sucesso": False, "erro": erro_msg}), 400

        dosagem = dados.get("dosagem", "").strip()
        if not dosagem:
            erro_msg = "Dosagem não pode ser vazia"
            return jsonify({"sucesso": False, "erro": erro_msg}), 400

        horario = dados.get("horario", "").strip()
        if not _validar_horario(horario):
            return jsonify({
                "sucesso": False,
                "erro": "Horário inválido. Use o formato HH:MM"
            }), 400

        dia = _normalizar_dia(dados.get("dia", "todos"))
        if dia not in DIAS_VALIDOS:
            return jsonify({
                "sucesso": False,
                "erro": "Dia inválido para o medicamento"
            }), 400

        conexao = get_conexao()
        cursor = conexao.cursor()

        observacao = dados.get("observacao", "").strip()

        cursor.execute(
            "INSERT INTO medicamentos "
            "(usuario_id, nome, dosagem, horario, dia, observacao) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (usuario_id, nome, dosagem, horario, dia, observacao),
        )

        conexao.commit()
        novo_id = cursor.lastrowid

        return jsonify({
            "sucesso": True,
            "mensagem": f"Medicamento '{nome}' cadastrado com sucesso!",
            "id": novo_id
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/<int:med_id>/marcar-tomado", methods=["POST"])
@login_required
def marcar_como_tomado(med_id):
    """Marca um medicamento como tomado hoje."""
    try:
        usuario_id = session["usuario_id"]
        hoje = _data_hoje()
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM medicamentos "
            "WHERE id = ? AND usuario_id = ? AND ativo = 1",
            (med_id, usuario_id),
        )
        medicamento = cursor.fetchone()

        if not medicamento:
            return jsonify({
                "sucesso": False,
                "erro": "Medicamento não encontrado ou inativo"
            }), 404

        cursor.execute(
            "SELECT id FROM registros_tomados "
            "WHERE medicamento_id = ? AND data_tomado = ?",
            (med_id, hoje),
        )
        if cursor.fetchone():
            med_name = medicamento['nome']
            erro_msg = f"'{med_name}' já foi marcado como tomado"
            return jsonify({
                "sucesso": False,
                "erro": erro_msg
            }), 400

        cursor.execute(
            "INSERT INTO registros_tomados (medicamento_id, data_tomado) "
            "VALUES (?, ?)",
            (med_id, hoje),
        )

        conexao.commit()

        return jsonify({
            "sucesso": True,
            "mensagem": f"'{medicamento['nome']}' marcado como tomado!"
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route(
    "/api/medicamentos/<int:med_id>/desmarcar-tomado",
    methods=["DELETE"],
)
@login_required
def desmarcar_como_tomado(med_id):
    """Remove o registro de medicamento tomado hoje (undo)."""
    try:
        usuario_id = session["usuario_id"]
        hoje = _data_hoje()
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM medicamentos "
            "WHERE id = ? AND usuario_id = ? AND ativo = 1",
            (med_id, usuario_id),
        )
        medicamento = cursor.fetchone()

        if not medicamento:
            return jsonify({
                "sucesso": False,
                "erro": "Medicamento não encontrado ou inativo"
            }), 404

        cursor.execute(
            "SELECT id FROM registros_tomados "
            "WHERE medicamento_id = ? AND data_tomado = ?",
            (med_id, hoje),
        )
        registro = cursor.fetchone()
        if not registro:
            med_name = medicamento["nome"]
            erro_msg = f"'{med_name}' não está marcado como tomado hoje"
            return jsonify({
                "sucesso": False,
                "erro": erro_msg
            }), 400

        cursor.execute(
            "DELETE FROM registros_tomados WHERE id = ?",
            (registro["id"],),
        )
        conexao.commit()

        return jsonify({
            "sucesso": True,
            "mensagem": f"Marcação de '{medicamento['nome']}' desfeita!"
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/<int:med_id>/remover", methods=["DELETE"])
@login_required
def remover_medicamento(med_id):
    """Remove (desativa) um medicamento."""
    try:
        usuario_id = session["usuario_id"]
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM medicamentos "
            "WHERE id = ? AND usuario_id = ?",
            (med_id, usuario_id),
        )
        medicamento = cursor.fetchone()

        if not medicamento:
            return jsonify({
                "sucesso": False,
                "erro": "Medicamento não encontrado"
            }), 404

        cursor.execute(
            "UPDATE medicamentos SET ativo = 0 WHERE id = ?",
            (med_id,),
        )

        conexao.commit()

        return jsonify({
            "sucesso": True,
            "mensagem": f"Medicamento '{medicamento['nome']}' removido!"
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/<int:med_id>/editar", methods=["PUT"])
@login_required
def editar_medicamento(med_id):
    """Atualiza os dados de um medicamento ativo."""
    try:
        usuario_id = session["usuario_id"]
        dados = request.get_json(silent=True)
        if dados is None:
            return jsonify({
                "sucesso": False,
                "erro": "JSON inválido ou ausente no corpo da requisição"
            }), 400

        nome = dados.get("nome", "").strip()
        if not nome:
            return jsonify({
                "sucesso": False,
                "erro": "Nome não pode ser vazio",
            }), 400

        dosagem = dados.get("dosagem", "").strip()
        if not dosagem:
            return jsonify({
                "sucesso": False,
                "erro": "Dosagem não pode ser vazia"
            }), 400

        horario = dados.get("horario", "").strip()
        if not _validar_horario(horario):
            return jsonify({
                "sucesso": False,
                "erro": "Horário inválido. Use o formato HH:MM"
            }), 400

        dia = _normalizar_dia(dados.get("dia", "todos"))
        if dia not in DIAS_VALIDOS:
            return jsonify({
                "sucesso": False,
                "erro": "Dia inválido para o medicamento"
            }), 400

        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id FROM medicamentos "
            "WHERE id = ? AND usuario_id = ? AND ativo = 1",
            (med_id, usuario_id),
        )
        if not cursor.fetchone():
            return jsonify({
                "sucesso": False,
                "erro": "Medicamento não encontrado ou inativo"
            }), 404

        observacao = dados.get("observacao", "").strip()

        cursor.execute(
            "UPDATE medicamentos "
            "SET nome = ?, dosagem = ?, horario = ?, dia = ?, observacao = ? "
            "WHERE id = ?",
            (nome, dosagem, horario, dia, observacao, med_id),
        )
        conexao.commit()

        return jsonify({
            "sucesso": True,
            "mensagem": f"Medicamento '{nome}' atualizado com sucesso!"
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/<nome>/consultar", methods=["GET"])
def consultar_medicamento(nome):
    """Consulta informações sobre um medicamento via Groq API."""
    try:
        resultado = buscar_medicamento_groq(nome)
        if resultado is None:
            return jsonify({
                "sucesso": False,
                "erro": "Medicamento não encontrado"
            }), 404

        resultado_info = resultado["informacoes"]
        informacoes_formatadas = formatar_resposta_medicamento(
            resultado_info
        )

        return jsonify({
            "sucesso": True,
            "medicamento": resultado["nome"],
            "informacoes": informacoes_formatadas
        })
    except APIError as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400
    except Exception:
        return jsonify({
            "sucesso": False,
            "erro": "Erro ao consultar informações do medicamento"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
