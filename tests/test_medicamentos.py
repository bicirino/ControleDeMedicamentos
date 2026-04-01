"""
tests/test_medicamentos.py
Testes automatizados para as funcoes principais do sistema.
"""

import pytest
from unittest.mock import patch
from datetime import datetime

import medicamentos


@pytest.fixture
def db_mock():
    """
    Fixture que substitui get_conexao por um banco SQLite em memoria.
    Cria as tabelas necessarias e devolve a conexao para uso nos testes.
    """
    import sqlite3

    conexao = sqlite3.connect(":memory:")
    conexao.row_factory = sqlite3.Row

    conexao.execute("""
        CREATE TABLE medicamentos (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            nome    TEXT    NOT NULL,
            dosagem TEXT    NOT NULL,
            horario TEXT    NOT NULL,
            ativo   INTEGER NOT NULL DEFAULT 1
        )
    """)
    conexao.execute("""
        CREATE TABLE registros_tomados (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            medicamento_id INTEGER NOT NULL,
            data_tomado    TEXT    NOT NULL,
            FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
        )
    """)
    conexao.commit()

    with patch("medicamentos.get_conexao") as mock_get_conexao:
        mock_get_conexao.return_value = conexao
        yield conexao

    conexao.close()


class TestCadastrarMedicamento:
    """Testes de cadastro de medicamentos."""

    def test_cadastro_valido(self, db_mock, capsys):
        """Cadastro com dados validos insere registro e exibe sucesso."""
        with patch("builtins.input",
                   side_effect=["Paracetamol", "500mg", "08:00"]):
            medicamentos.cadastrar_medicamento()

        cursor = db_mock.execute("SELECT * FROM medicamentos")
        resultado = cursor.fetchall()

        assert len(resultado) == 1
        assert resultado[0]["nome"] == "Paracetamol"
        assert resultado[0]["dosagem"] == "500mg"
        assert resultado[0]["horario"] == "08:00"
        assert resultado[0]["ativo"] == 1

        saida = capsys.readouterr().out
        assert "cadastrado com sucesso" in saida

    def test_cadastro_nome_vazio(self, db_mock, capsys):
        """Nome vazio nao insere registro e exibe aviso."""
        with patch("builtins.input", side_effect=[""]):
            medicamentos.cadastrar_medicamento()

        cursor = db_mock.execute("SELECT * FROM medicamentos")
        assert cursor.fetchone() is None

        saida = capsys.readouterr().out
        assert "vazio" in saida

    def test_cadastro_horario_invalido(self, db_mock, capsys):
        """Horario fora do formato HH:MM nao insere e exibe aviso."""
        with patch("builtins.input",
                   side_effect=["Dipirona", "1 comprimido", "8h"]):
            medicamentos.cadastrar_medicamento()

        cursor = db_mock.execute("SELECT * FROM medicamentos")
        assert cursor.fetchone() is None

        saida = capsys.readouterr().out
        assert "invalido" in saida


class TestListarMedicamentosoDoDia:
    """Testes de listagem diaria de medicamentos."""

    def test_listagem_sem_medicamentos(self, db_mock, capsys):
        """Banco vazio exibe mensagem informativa."""
        medicamentos.listar_medicamentos_do_dia()

        saida = capsys.readouterr().out
        assert "Nenhum medicamento" in saida

    def test_listagem_com_medicamento_pendente(self, db_mock, capsys):
        """Medicamento ativo nao tomado aparece como Pendente."""
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            ("Losartana", "50mg", "07:00"),
        )
        db_mock.commit()

        medicamentos.listar_medicamentos_do_dia()

        saida = capsys.readouterr().out
        assert "Losartana" in saida
        assert "Pendente" in saida

    def test_listagem_com_medicamento_tomado(self, db_mock, capsys):
        """Medicamento ja registrado hoje aparece como Tomado."""
        hoje = datetime.now().strftime("%Y-%m-%d")

        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            ("Atenolol", "25mg", "12:00"),
        )
        db_mock.commit()

        cursor = db_mock.execute(
            "SELECT id FROM medicamentos WHERE nome = 'Atenolol'"
        )
        med_id = cursor.fetchone()["id"]

        db_mock.execute(
            "INSERT INTO registros_tomados (medicamento_id, data_tomado) "
            "VALUES (?, ?)",
            (med_id, hoje),
        )
        db_mock.commit()

        medicamentos.listar_medicamentos_do_dia()

        saida = capsys.readouterr().out
        assert "Atenolol" in saida
        assert "Tomado" in saida


class TestMarcarComoTomado:
    """Testes de registro de medicamento tomado."""

    def test_marcar_medicamento_valido(self, db_mock, capsys):
        """ID valido registra o medicamento e exibe sucesso."""
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            ("Metformina", "850mg", "13:00"),
        )
        db_mock.commit()

        cursor = db_mock.execute(
            "SELECT id FROM medicamentos WHERE nome = 'Metformina'"
        )
        med_id = cursor.fetchone()["id"]

        with patch("builtins.input", side_effect=[str(med_id)]):
            medicamentos.marcar_como_tomado()

        hoje = datetime.now().strftime("%Y-%m-%d")
        cursor = db_mock.execute(
            "SELECT * FROM registros_tomados "
            "WHERE medicamento_id = ? AND data_tomado = ?",
            (med_id, hoje),
        )
        assert cursor.fetchone() is not None

        saida = capsys.readouterr().out
        assert "marcado como tomado" in saida

    def test_marcar_medicamento_duplicado(self, db_mock, capsys):
        """Marcar o mesmo medicamento duas vezes no dia nao duplica registro."""
        hoje = datetime.now().strftime("%Y-%m-%d")

        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            ("Omeprazol", "20mg", "07:30"),
        )
        db_mock.commit()

        cursor = db_mock.execute(
            "SELECT id FROM medicamentos WHERE nome = 'Omeprazol'"
        )
        med_id = cursor.fetchone()["id"]

        db_mock.execute(
            "INSERT INTO registros_tomados (medicamento_id, data_tomado) "
            "VALUES (?, ?)",
            (med_id, hoje),
        )
        db_mock.commit()

        with patch("builtins.input", side_effect=[str(med_id)]):
            medicamentos.marcar_como_tomado()

        cursor = db_mock.execute(
            "SELECT COUNT(*) as total FROM registros_tomados "
            "WHERE medicamento_id = ? AND data_tomado = ?",
            (med_id, hoje),
        )
        assert cursor.fetchone()["total"] == 1

        saida = capsys.readouterr().out
        assert "ja foi marcado" in saida

    def test_marcar_id_invalido(self, db_mock, capsys):
        """Texto no campo de ID exibe aviso e nao insere registro."""
        with patch("builtins.input", side_effect=["abc"]):
            medicamentos.marcar_como_tomado()

        saida = capsys.readouterr().out
        assert "invalido" in saida


class TestRemoverMedicamento:
    """Testes de remocao (soft delete) de medicamentos."""

    def test_remover_com_confirmacao(self, db_mock, capsys):
        """Confirmacao com 's' desativa o medicamento (ativo = 0)."""
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            ("Rivotril", "2mg", "22:00"),
        )
        db_mock.commit()

        cursor = db_mock.execute(
            "SELECT id FROM medicamentos WHERE nome = 'Rivotril'"
        )
        med_id = cursor.fetchone()["id"]

        with patch("builtins.input", side_effect=[str(med_id), "s"]):
            medicamentos.remover_medicamento()

        cursor = db_mock.execute(
            "SELECT ativo FROM medicamentos WHERE id = ?", (med_id,)
        )
        assert cursor.fetchone()["ativo"] == 0

        saida = capsys.readouterr().out
        assert "removido com sucesso" in saida

    def test_remover_sem_confirmacao(self, db_mock, capsys):
        """Resposta 'n' cancela a remocao e mantem medicamento ativo."""
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) "
            "VALUES (?, ?, ?)",
            ("Clonazepam", "1mg", "21:00"),
        )
        db_mock.commit()

        cursor = db_mock.execute(
            "SELECT id FROM medicamentos WHERE nome = 'Clonazepam'"
        )
        med_id = cursor.fetchone()["id"]

        with patch("builtins.input", side_effect=[str(med_id), "n"]):
            medicamentos.remover_medicamento()

        cursor = db_mock.execute(
            "SELECT ativo FROM medicamentos WHERE id = ?", (med_id,)
        )
        assert cursor.fetchone()["ativo"] == 1

        saida = capsys.readouterr().out
        assert "cancelada" in saida