import sqlite3
from datetime import datetime

DB_NAME = "medicamentos.db"


def get_conexao() -> sqlite3.Connection:
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco() -> None:
    conexao = get_conexao()
    cursor = conexao.cursor()

    # Criar tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT    UNIQUE NOT NULL,
            nome        TEXT    NOT NULL,
            senha_hash  TEXT    NOT NULL,
            criado_em   TEXT    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id  INTEGER NOT NULL,
            nome        TEXT    NOT NULL,
            dosagem     TEXT    NOT NULL,
            horario     TEXT    NOT NULL,
            dia         TEXT    NOT NULL DEFAULT 'todos',
            ativo       INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    # Migração para bancos criados antes da coluna `usuario_id`.
    cursor.execute("PRAGMA table_info(medicamentos)")
    colunas = {linha["name"] for linha in cursor.fetchall()}
    if "usuario_id" not in colunas:
        # Criar tabela temporária com a nova estrutura
        cursor.execute("""
            CREATE TABLE medicamentos_temp (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id  INTEGER NOT NULL,
                nome        TEXT    NOT NULL,
                dosagem     TEXT    NOT NULL,
                horario     TEXT    NOT NULL,
                dia         TEXT    NOT NULL DEFAULT 'todos',
                ativo       INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)
        
        # Se houver dados existentes, criar usuário padrão e migrar
        cursor.execute("SELECT COUNT(*) as cnt FROM medicamentos")
        tem_dados = cursor.fetchone()["cnt"] > 0
        
        if tem_dados:
            # Criar usuário padrão para dados existentes
            try:
                from datetime import datetime
                from werkzeug.security import generate_password_hash
                
                cursor.execute(
                    "INSERT INTO usuarios (email, nome, senha_hash, criado_em) "
                    "VALUES (?, ?, ?, ?)",
                    (
                        "padrão@local",
                        "Usuário Padrão",
                        generate_password_hash("mudeSenha123"),
                        datetime.now().isoformat()
                    )
                )
                usuario_id = cursor.lastrowid
                
                # Copiar dados existentes
                cursor.execute(
                    "INSERT INTO medicamentos_temp "
                    "(usuario_id, nome, dosagem, horario, dia, ativo) "
                    "SELECT ?, nome, dosagem, horario, dia, ativo "
                    "FROM medicamentos"
                )
            except Exception:
                # Se falhar, usar usuario_id = 1
                cursor.execute(
                    "INSERT INTO medicamentos_temp "
                    "(usuario_id, nome, dosagem, horario, dia, ativo) "
                    "SELECT 1, nome, dosagem, horario, dia, ativo "
                    "FROM medicamentos"
                )
        
        # Remover tabela antiga e renomear
        cursor.execute("DROP TABLE medicamentos")
        cursor.execute(
            "ALTER TABLE medicamentos_temp RENAME TO medicamentos"
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
