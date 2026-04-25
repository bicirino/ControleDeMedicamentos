"""
app.py
Aplicação Flask para interface web do Controle de Medicamentos.
Expõe endpoints REST que integram com a lógica de negócio existente.
"""

import re
from flask import Flask, render_template, request, jsonify
from database import get_conexao, inicializar_banco
from medicamentos import (
    _data_hoje,
    _validar_horario,
)
from api_integration import buscar_medicamento_groq, APIError

app = Flask(__name__)

# Inicializar banco ao iniciar a aplicação
inicializar_banco()


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
    texto = re.sub(r'^• ([A-Z][^:]*?):\s', r'• <strong>\1</strong>: ', texto, flags=re.MULTILINE)
    
    return texto.strip()


@app.route("/")
def index():
    """Renderiza a página principal."""
    return render_template("index.html")


@app.route("/api/medicamentos/dia", methods=["GET"])
def get_medicamentos_dia():
    """Retorna medicamentos do dia com status de tomado."""
    try:
        hoje = _data_hoje()
        conexao = get_conexao()
        
        with get_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, dosagem, horario "
                "FROM medicamentos WHERE ativo = 1 ORDER BY horario"
            )
            medicamentos = cursor.fetchall()
            cursor.execute(
                "SELECT medicamento_id FROM registros_tomados WHERE data_tomado = ?",
                (hoje,),
            )
            ids_tomados = {row["medicamento_id"] for row in cursor.fetchall()}

        resultado = []
        for med in medicamentos:
            resultado.append({
                "id": med["id"],
                "nome": med["nome"],
                "dosagem": med["dosagem"],
                "horario": med["horario"],
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
def get_todos_medicamentos():
    """Retorna todos os medicamentos cadastrados (apenas ativos)."""
    try:
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id, nome, dosagem, horario, ativo "
            "FROM medicamentos WHERE ativo = 1 ORDER BY horario"
        )
        medicamentos = cursor.fetchall()

        resultado = []
        for med in medicamentos:
            resultado.append({
                "id": med["id"],
                "nome": med["nome"],
                "dosagem": med["dosagem"],
                "horario": med["horario"],
                "ativo": med["ativo"] == 1
            })

        return jsonify({
            "sucesso": True,
            "medicamentos": resultado
        })
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500


@app.route("/api/medicamentos/cadastrar", methods=["POST"])
def cadastrar_medicamento():
    """Cadastra um novo medicamento."""
    try:
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

        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            (nome, dosagem, horario),
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
def marcar_como_tomado(med_id):
    """Marca um medicamento como tomado hoje."""
    try:
        hoje = _data_hoje()
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM medicamentos WHERE id = ? AND ativo = 1",
            (med_id,),
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


@app.route("/api/medicamentos/<int:med_id>/remover", methods=["DELETE"])
def remover_medicamento(med_id):
    """Remove (desativa) um medicamento."""
    try:
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM medicamentos WHERE id = ?",
            (med_id,),
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
        
        informacoes_formatadas = formatar_resposta_medicamento(resultado["informacoes"])
        
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
    app.run(debug=True, port=5000)
