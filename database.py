import os
import sqlite3
from datetime import datetime
from typing import Optional

_DEFAULT_DB = os.path.join(os.path.dirname(__file__), "medicamentos.db")


def _resolver_db_path() -> str:
    """Resolve o caminho do banco SQLite, priorizando persistencia local."""
    env_path = os.environ.get("DB_PATH")
    if env_path:
        return env_path

    # Render/containers com disco persistente montado em /var/data
    if os.path.isdir("/var/data"):
        return os.path.join("/var/data", "medicamentos.db")

    return _DEFAULT_DB


def _obter_database_url() -> Optional[str]:
    return os.environ.get("DATABASE_URL") or os.environ.get("SUPABASE_DB_URL")


DB_NAME = _resolver_db_path()
DATABASE_URL = _obter_database_url()
DB_KIND = "postgres" if DATABASE_URL else "sqlite"

_db_dir = os.path.dirname(DB_NAME)
if _db_dir and DB_KIND == "sqlite":
    os.makedirs(_db_dir, exist_ok=True)


def _adaptar_sql(sql: str) -> str:
    return sql.replace("?", "%s")


def _deve_retornar_id(sql: str) -> bool:
    sql_upper = sql.lstrip().upper()
    return sql_upper.startswith("INSERT") and "RETURNING" not in sql_upper


class _DBCursor:
    def __init__(self, cursor, db_kind: str) -> None:
        self._cursor = cursor
        self._db_kind = db_kind
        self._lastrowid = None

    def execute(self, sql: str, params=None):
        if params is None:
            params = ()

        if self._db_kind == "postgres":
            sql = _adaptar_sql(sql)
            if _deve_retornar_id(sql):
                sql = f"{sql} RETURNING id"
                self._cursor.execute(sql, params)
                row = self._cursor.fetchone()
                if row is not None:
                    if isinstance(row, dict):
                        self._lastrowid = row.get("id")
                    else:
                        self._lastrowid = row[0]
                return self

        self._cursor.execute(sql, params)
        return self

    def executemany(self, sql: str, seq_of_params):
        if self._db_kind == "postgres":
            sql = _adaptar_sql(sql)
        self._cursor.executemany(sql, seq_of_params)
        return self

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    @property
    def lastrowid(self):
        if self._db_kind == "postgres":
            return self._lastrowid
        return self._cursor.lastrowid

    def __getattr__(self, item):
        return getattr(self._cursor, item)


class _DBConnection:
    def __init__(self, conn, db_kind: str) -> None:
        self._conn = conn
        self._db_kind = db_kind

    def cursor(self):
        return _DBCursor(self._conn.cursor(), self._db_kind)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            try:
                self._conn.rollback()
            finally:
                self._conn.close()
            return False

        try:
            self._conn.commit()
        finally:
            self._conn.close()
        return False

    def __getattr__(self, item):
        return getattr(self._conn, item)


def get_conexao():
    if DB_KIND == "postgres":
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Dependencia 'psycopg' nao encontrada. "
                "Instale com: pip install -r requirements.txt"
            ) from exc

        conexao = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        return _DBConnection(conexao, DB_KIND)

    conexao = sqlite3.connect(DB_NAME, timeout=10)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.execute("PRAGMA journal_mode = WAL")
    return _DBConnection(conexao, DB_KIND)


def _inicializar_sqlite(conexao) -> None:
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
            # Se ALTER TABLE falhar por qualquer razão, ignorar (não crítico)
            pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_tomados (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            medicamento_id   INTEGER NOT NULL,
            data_tomado      TEXT    NOT NULL,
            FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
        )
    """)


def _inicializar_postgres(conexao) -> None:
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id          SERIAL PRIMARY KEY,
            email       TEXT    UNIQUE NOT NULL,
            nome        TEXT    NOT NULL,
            senha_hash  TEXT    NOT NULL,
            criado_em   TEXT    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id          SERIAL PRIMARY KEY,
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_tomados (
            id               SERIAL PRIMARY KEY,
            medicamento_id   INTEGER NOT NULL,
            data_tomado      TEXT    NOT NULL,
            FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
        )
    """)


def inicializar_banco() -> None:
    conexao = get_conexao()
    if DB_KIND == "postgres":
        _inicializar_postgres(conexao)
    else:
        _inicializar_sqlite(conexao)
    conexao.commit()
    conexao.close()
