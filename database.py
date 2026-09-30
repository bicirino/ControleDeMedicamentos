import os
import sqlite3
from datetime import datetime
from contextlib import contextmanager

# Detectar tipo de banco
DATABASE_URL = os.environ.get("DATABASE_URL") or None
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg
    from psycopg import rows
else:
    # SQLite local
    _DEFAULT_DB = os.path.join(
        os.path.dirname(__file__), "medicamentos.db"
    )
    DB_NAME = os.environ.get("DB_PATH", _DEFAULT_DB)
    _db_dir = os.path.dirname(DB_NAME)
    if _db_dir:
        os.makedirs(_db_dir, exist_ok=True)


class Row(dict):
    """Adapter para fazer PostgreSQL rows behave like sqlite3.Row"""
    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)


def _adapt_query(query: str) -> str:
    """Converte placeholders do SQLite para PostgreSQL quando necessario."""
    if USE_POSTGRES:
        return query.replace("?", "%s")
    return query


class _CursorAdapter:
    """Cursor com adaptacao de placeholders para PostgreSQL."""
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        query = _adapt_query(query)
        if params is None:
            return self._cursor.execute(query)
        return self._cursor.execute(query, params)

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class _ConnectionAdapter:
    """Conexao com cursor adaptado para PostgreSQL."""
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return _CursorAdapter(self._conn.cursor(row_factory=rows.dict_row))

    def execute(self, query, params=None):
        query = _adapt_query(query)
        if params is None:
            return self._conn.execute(query)
        return self._conn.execute(query, params)

    def __getattr__(self, name):
        return getattr(self._conn, name)


@contextmanager
def get_conexao():
    """Gerenciador de contexto para conexão de banco"""
    if USE_POSTGRES:
        conn = psycopg.connect(DATABASE_URL)
        conn.autocommit = False
        try:
            yield _ConnectionAdapter(conn)
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(DB_NAME, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
        finally:
            conn.close()


def inicializar_banco() -> None:
    """Inicializa banco de dados (SQLite ou PostgreSQL)"""
    if USE_POSTGRES:
        _inicializar_postgres()
    else:
        _inicializar_sqlite()


def _inicializar_postgres() -> None:
    """Inicializa schema no PostgreSQL"""
    with get_conexao() as conexao:
        cursor = conexao.cursor()

        # Criar tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id          SERIAL PRIMARY KEY,
                email       TEXT UNIQUE NOT NULL,
                nome        TEXT NOT NULL,
                senha_hash  TEXT NOT NULL,
                criado_em   TEXT NOT NULL
            )
        """)

        # Criar tabela de medicamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicamentos (
                id          SERIAL PRIMARY KEY,
                usuario_id  INTEGER NOT NULL REFERENCES usuarios(id),
                nome        TEXT NOT NULL,
                dosagem     TEXT NOT NULL,
                horario     TEXT NOT NULL,
                dia         TEXT NOT NULL DEFAULT 'todos',
                observacao  TEXT DEFAULT '',
                ativo       INTEGER NOT NULL DEFAULT 1
            )
        """)

        # Criar tabela de registros tomados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros_tomados (
                id              SERIAL PRIMARY KEY,
                medicamento_id  INTEGER NOT NULL
                                REFERENCES medicamentos(id),
                data_tomado     TEXT NOT NULL
            )
        """)

        conexao.commit()


def _inicializar_sqlite() -> None:
    """Inicializa schema no SQLite"""
    conexao = sqlite3.connect(DB_NAME, timeout=10)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.execute("PRAGMA journal_mode = WAL")
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
            observacao  TEXT    DEFAULT '',
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
                from werkzeug.security import generate_password_hash

                cursor.execute(
                    "INSERT INTO usuarios (email, nome, senha_hash, "
                    "criado_em) VALUES (?, ?, ?, ?)",
                    (
                        "padrão@local",
                        "Usuário Padrão",
                        generate_password_hash("mudeSenha123"),
                        datetime.now().isoformat(),
                    )
                )

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

    # Garantir coluna `observacao` em bancos antigos
    cursor.execute("PRAGMA table_info(medicamentos)")
    colunas = {linha["name"] for linha in cursor.fetchall()}
    if "observacao" not in colunas:
        try:
            cursor.execute(
                "ALTER TABLE medicamentos ADD COLUMN observacao TEXT "
                "DEFAULT ''"
            )
        except Exception:
            pass

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
