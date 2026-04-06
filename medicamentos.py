"""
medicamentos.py
Logica de negocio para cadastro, listagem, registro e remocao de medicamentos.
"""

from datetime import datetime

from database import get_conexao


def _data_hoje() -> str:
    """Retorna a data atual no formato YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def _validar_horario(horario: str) -> bool:
    """
    Valida se o horario esta no formato HH:MM.

    Args:
        horario: String com o horario informado pelo usuario.

    Returns:
        True se valido, False caso contrario.
    """
    try:
        datetime.strptime(horario, "%H:%M")
        return True
    except ValueError:
        return False


def cadastrar_medicamento() -> None:
    """Solicita os dados ao usuario e cadastra um novo medicamento."""
    print()
    nome = input("📋 Nome do medicamento: ").strip()
    if not nome:
        print("⚠️  O nome nao pode ser vazio.\n")
        return

    dosagem = input("💊 Dosagem (ex: 500mg, 1 comprimido): ").strip()
    if not dosagem:
        print("⚠️  A dosagem nao pode ser vazia.\n")
        return

    horario = input("🕐 Horario de tomar (HH:MM): ").strip()
    if not _validar_horario(horario):
        print("⚠️  Horario invalido. Use o formato HH:MM (ex: 08:00).\n")
        return

    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO medicamentos (nome, dosagem, horario) VALUES (?, ?, ?)",
        (nome, dosagem, horario),
    )

    conexao.commit()

    print(f"\n✅ Medicamento '{nome}' cadastrado com sucesso!\n")


def listar_medicamentos_do_dia() -> None:
    """Lista todos os medicamentos ativos e indica quais ja foram tomados."""
    hoje = _data_hoje()

    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, dosagem, horario "
        "FROM medicamentos WHERE ativo = 1 ORDER BY horario"
    )
    medicamentos = cursor.fetchall()

    if not medicamentos:
        print("\n📭 Nenhum medicamento cadastrado.\n")
        return

    cursor.execute(
        "SELECT medicamento_id FROM registros_tomados WHERE data_tomado = ?",
        (hoje,),
    )
    ids_tomados = {row["medicamento_id"] for row in cursor.fetchall()}

    print(f"\n📅 Medicamentos para hoje ({hoje}):\n")
    print(f"  {'ID':<5} {'Horario':<10} {'Medicamento':<25} "
          f"{'Dosagem':<20} {'Status'}")
    print("  " + "─" * 70)

    for med in medicamentos:
        status = "✅ Tomado" if med["id"] in ids_tomados else "⏳ Pendente"
        print(
            f"  {med['id']:<5} {med['horario']:<10} {med['nome']:<25} "
            f"{med['dosagem']:<20} {status}"
        )

    print()


def marcar_como_tomado() -> None:
    """Registra que um medicamento foi tomado no dia atual."""
    listar_medicamentos_do_dia()

    hoje = _data_hoje()
    conexao = get_conexao()
    cursor = conexao.cursor()

    try:
        med_id = int(input("🔢 Informe o ID do medicamento tomado: ").strip())
    except ValueError:
        print("⚠️  ID invalido. Digite apenas numeros.\n")
        return

    cursor.execute(
        "SELECT nome FROM medicamentos WHERE id = ? AND ativo = 1",
        (med_id,),
    )
    medicamento = cursor.fetchone()

    if not medicamento:
        print("⚠️  Medicamento nao encontrado ou inativo.\n")
        return

    cursor.execute(
        "SELECT id FROM registros_tomados "
        "WHERE medicamento_id = ? AND data_tomado = ?",
        (med_id, hoje),
    )
    if cursor.fetchone():
        msg = f"ℹ️  '{medicamento['nome']}' ja foi marcado como tomado hoje.\n"
        print(msg)
        return

    cursor.execute(
        "INSERT INTO registros_tomados (medicamento_id, data_tomado) "
        "VALUES (?, ?)",
        (med_id, hoje),
    )

    conexao.commit()

    print(f"\n✅ '{medicamento['nome']}' marcado como tomado!\n")


def listar_todos_medicamentos() -> None:
    """Lista todos os medicamentos cadastrados, incluindo inativos."""
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, dosagem, horario, ativo "
        "FROM medicamentos ORDER BY horario"
    )
    medicamentos = cursor.fetchall()

    if not medicamentos:
        print("\n📭 Nenhum medicamento cadastrado.\n")
        return

    print("\n📋 Todos os medicamentos cadastrados:\n")
    print(f"  {'ID':<5} {'Horario':<10} {'Medicamento':<25} "
          f"{'Dosagem':<20} {'Situacao'}")
    print("  " + "─" * 70)

    for med in medicamentos:
        situacao = "🟢 Ativo" if med["ativo"] == 1 else "🔴 Inativo"
        print(
            f"  {med['id']:<5} {med['horario']:<10} {med['nome']:<25} "
            f"{med['dosagem']:<20} {situacao}"
        )

    print()


def remover_medicamento() -> None:
    """
    Desativa um medicamento (soft delete).
    O registro permanece no banco para preservar o historico.
    """
    listar_todos_medicamentos()

    conexao = get_conexao()
    cursor = conexao.cursor()

    try:
        med_id = int(
            input("🔢 Informe o ID do medicamento a remover: ").strip()
        )
    except ValueError:
        print("⚠️  ID invalido. Digite apenas numeros.\n")
        return

    cursor.execute(
        "SELECT nome FROM medicamentos WHERE id = ? AND ativo = 1",
        (med_id,),
    )
    medicamento = cursor.fetchone()

    if not medicamento:
        print("⚠️  Medicamento nao encontrado ou ja esta inativo.\n")
        return

    confirmacao = input(
        f"⚠️  Deseja remover '{medicamento['nome']}'? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("❌ Remocao cancelada.\n")
        return

    cursor.execute(
        "UPDATE medicamentos SET ativo = 0 WHERE id = ?",
        (med_id,),
    )

    conexao.commit()

    print(f"\n✅ '{medicamento['nome']}' removido com sucesso!\n")
