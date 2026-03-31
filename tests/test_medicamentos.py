import pytest 
from unittest.mock import patch, MagicMock 
from datetime import datetime 

import medicamentos

@pytest.fixture 
def db_mock(): 
    import sqlite3 
    
    conexao = sqlite3.connect(":memory:")
    conexao.row_factory = sqlite3.Row
    
    conexao.execute(""" 
        CREATE TABLE medicamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT NOT NULL, 
            dosagem     TEXT NOT NULL,
            horario     TEXT NOT NULL, 
            ativo       INTEGER NOT NULL DEFAULT 1 
        )
        
    """)
    
    conexao.execute("""
        CREATE TABLE registro_tomados (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            medicamento_id  INTEGER NOT NULL, 
            data_tomado     TEXT NOT NULL, 
            FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id)
        )
    """)
    
    conexao.commit() 
    
    with patch("medicamentos.get_conexao") as mock_get_conexao: 
        mock_get_conexao.return_value = conexao 
        
        yield conexao 
    
    conexao.close()
    
    

class TestCadastrarMedicamento: 
    
    def test_cadastro_valido(self, db_mock, capsys): 
        with patch("builtins.input", side_effect=["Paracetamol", "500mg", "08:00"]): 
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
        with patch("builtins.input", side_effect=[""]): 
            medicamentos.cadastrar_medicamento() 
            
        cursor = db_mock.execute("SELECT * FROM medicamentos")
        assert cursor.fetchone() is None
        
        saida = capsys.readouterr().out
        assert "vazio" in saida
    
    
    def test_cadastro_horario_invalido(self, db_mock, capsys): 
        with patch("builtins.input", side_effect=["Paracetamol", "500mg", "8h"]): 
            medicamentos.cadastrar_medicamento() 
            
        cursor = db_mock.execute("SELECT * FROM medicamentos")
        assert cursor.fetchone() is None 
        
        saida = capsys.readouterr().out
        assert "Horário inválido" in saida
        

class TestListarMedicamentosDoDia: 
    
    def test_linguagem_sem_medicamentos(self, db_mock, capsys): 
        medicamentos.listar_medicamento_do_dia() 
        
        saida = capsys.readouterr().out 
        assert "Nenhum medicamento cadastrado" in saida 
        
    def test_linguagem_com_medicamento(self,db_mock, capsys): 
        
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)", 
            ("Losartana", "50mg", "07:00"), 
        )
        
        db_mock.commit() 
        
        medicamentos.listar_medicamento_do_dia() 
        
        saida = capsys.readouterr().out 
        assert "Losartana" in saida 
        assert "Pendente" in saida 
        
    def test_linguagem_com_medicamento_tomado(self, db_mock, capsys): 
        
        hoje = datetime.now().strftime("%Y-%m-%d")
        
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)", 
            ("Losartana", "50mg", "07:00"), 
        )
        db_mock.commit() 
        
        cursor = db_mock.execute ("SELECT id FROM medicamentos WHERE nome = 'Losartana'")
        med_id = cursor.fetchone()["id"]
        
        db_mock.execute(
            "INSERT INTO registro_tomados (medicamento_id, data_tomado) VALUES (?, ?)", 
            (med_id, hoje),
        )
        
        db_mock.commit() 
        
        medicamentos.listar_medicamento_do_dia() 
        
        saida = capsys.readouterr().out 
        assert "Losartana" in saida 
        assert "Tomado" in saida 
        
        
class TestMarcarComoTomado: 
    
    def test_marcar_medicamento_valido(self, db_mock, capsys): 
        
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)", 
            ("Paracetamol", "500mg", "13:00"),
        )
        
        db_mock.commit() 
        
        cursor = db_mock.execute("SELECT id FROM medicamentos WHERE nome = 'Paracetamol'")
        med_id = cursor.fetchone()["id"]
        
        with patch("builtins.input", return_values=str(med_id)): 
            medicamentos.marcar_como_tomado() 
            
        hoje = datetime.now().strftime("%Y-%m-%d")
        cursor = db_mock.execute(
            "SELECT * FROM registros_tomados WHERE medicamento_id = ? AND data_tomado = ?", 
            (med_id, hoje),  
        )
        assert cursor.fetchone() is not None 
        
        saida = capsys.readouterr().out 
        assert "marcado como tomado" in saida 
        
    def test_marcar_medicamento_duplicado(self, db_mock, capsys): 
        hoje = datetime.now().strftime("%Y-%m-%d")
        
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)", 
            ("Omeprazol", "20mg", "07:30"),
        )
        db_mock.commit() 
        
        cursor = db_mock.execute("SELECT id FROM medicamentos WHERE nome = 'Omeprazol'")
        med_id = cursor.fetchone()["id"]
        
        db_mock.execute(
            "INSERT INTO registros_tomados (medicamento_id, data_tomado) VALUES (?, ?)", 
            (med_id, hoje), 
        ) 
        db_mock.commit() 
        
        with patch("builtins.input", side_effect=[str(med_id)]): 
            medicamentos.marcar_como_tomado()
        
        cursor = db_mock.execute(
            "SELECT COUNT(*) as total FROM registros_tomados WHERE medicamento_id = ? AND data_tomado = ?", 
            (med_id, hoje),
        )
        assert cursor.fetchone()["total"] == 1
        
        saida = capsys.readouterr().out 
        assert "Medicamento já marcado como tomado" in saida 
        
    def test_marcar_id_invalido(self, db_mock, capsys): 
        with patch("builtins.input", side_effect=["abc"]): 
            medicamentos.marcar_como_tomado() 
        
        saida = capsys.readouterr().out 
        assert "inválido" in saida 
        

class TestRemoverMedicamento: 
    
    def test_remover_com_confirmacao(self, db_mock, capsys): 
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)",
            ("Rivotril", "2mg", "09:00"),
        )
        db_mock.commit() 
        
        cursor = db_mock.execute("SELECT id FROM medicamentos WHERE nome = 'Rivotril'")
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
        db_mock.execute(
            "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)",
            ("Clonazepam", "1mg", "22:00"),
        )
        db_mock.commit() 
        
        cursor = db_mock.execute("SELECT id FROM medicamentos WHERE nome = 'Clonazepam'")
        med_id = cursor.fetchone()["id"]
        
        with patch("builtings.input", side_effect=[str(med_id), "n"]): 
            medicamentos.remover_medicamento()
            
        cursor = db_mock.execute( 
            "SELECT ativo FROM medicamentos WHERE id = ?", (med_id,)
        )
        assert cursor.fetchone()["ativo"] == 1
        
        saida = capsys.readouterr().out 
        assert "cancelada" in saida