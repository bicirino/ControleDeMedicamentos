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
            dia         TEXT    NOT NULL DEFAULT 'todos',
            ativo       INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Migração para bancos criados antes da coluna `dia`.
    cursor.execute("PRAGMA table_info(medicamentos)")
    colunas = {linha["name"] for linha in cursor.fetchall()}
    if "dia" not in colunas:
        cursor.execute(
            "ALTER TABLE medicamentos "
            "ADD COLUMN dia TEXT NOT NULL DEFAULT 'todos'"
        )

    cursor.execute(
        "UPDATE medicamentos SET dia = 'todos' "
        "WHERE dia IS NULL OR TRIM(dia) = ''"
    )

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
