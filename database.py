import sqlite3

DB_NAME = "medicamentos.db"


def get_conexao() -> sqlite3.Connection:
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco() -> None:
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT    NOT NULL,
            dosagem     TEXT    NOT NULL,
            horario     TEXT    NOT NULL,
            ativo       INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_tomados (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            medicamento_id   INTEGER NOT NULL,
            data_tomado      TEXT    NOT NULL,
            FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
        )
    """)

    conexao.commit()
    conexao.close()
