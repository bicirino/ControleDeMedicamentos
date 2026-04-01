from datetime import datetime 
from database import get_conexao 

def _data_hoje() -> str: 
    return datetime.now().strftime("%Y-%m-%d") 


def _validar_horario(horario: str) -> bool: 

    try: 
        datetime.strptime(horario, "%H:%M")
        return True 
    except ValueError: 
        return False 

def cadastrar_medicamento() -> None: 
    print() 
    nome = input ("Nome do medicamento: ").strip() 

    if not nome: 
        print("O nome não pode ser vazio! \n")
        return 

    dosagem = input("Dosagem (ex: 500mg, 1 comprimido):").strip() 
    if not dosagem: 
        print("A dosagem não pode ser vazia! \n")
        return 

    horario = input("Horário de tomar (HH:MM):").strip() 
    if not _validar_horario(horario): 
        print("Horário inválido. Use o formato HH:MM (ex: 08:00) \n")
        return 
    
    conexao = get_conexao() 
    cursor = conexao.cursor() 

    cursor.execute( 
        "INSERT INTO medicamento (nome, dosagem, horario) VALUES (?, ?, ?)", 
        (nome,dosagem, horario), 
    ) 

    conexao.commit() 
    conexao.close() 

    print(f"Medicamento '{nome}' cadastrado com sucesso! \n")

def listar_medicamento_do_dia() -> None: 
    hoje = _data_hoje() 

    conexao = get_conexao() 
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, dosagem, horario FROM medicamentos WHERE ativo = 1 ORDER BY horario"
    )
    medicamentos = cursor.fetchall() 

    if not medicamentos: 
        print("Nenhum medicamento cadastrado \n ")
        conexao.close() 
        return 

    cursor.execute(
        "SELECT medicamento_id FROM registro_tomados WHERE data_tomado = ?",
        (hoje,), 

    ) 
    ids_tomados = {row["medicamento_id"] for row in cursor.fetchall() }
    conexao.close() 

    print(f"Medicamentos para hoje: ({hoje}): \n ")
    print(f"  {'ID':<5} {'Horário':<10} {'Medicamento':<25} {'Dosagem':<20} {'Status'}")
    print("  " + "─" * 70)

    for med in medicamentos: 
        status = "Tomado" if med["id"] in ids_tomados else "Pendente"
        print(
            f"  {med['id']:<5} {med['horario']:<10} {med['nome']:<25} {med['dosagem']:<20} {status}"
        )
    print() 


def marcar_como_tomado() -> None: 
    listar_medicamento_do_dia() 

    hoje = _data_hoje() 
    conexao = get_conexao() 
    cursor = conexao.cursor() 

    try: 
        med_id = int(input("Informe o ID do medicamento tomado: ").strip())
    except ValueError: 
        print("ID inválido. Digite apenas números \n")
        conexao.close() 
        return 


    cursor.execute(
        "SELECT nome FROM medicamentos WHERE id = ? AND ativo = 1", 
        (med_id,), 
    ) 
    medicamento = cursor.fetchone() 

    if not medicamento: 
        print ("Medicamento não encontrado ou inativo")
        conexao.close() 
        return 

    cursor.execute(
        "SELECT id FROM registros_tomados WHERE medicamento_id = ? AND data_tomado = ?", 
        (med_id, hoje), 
    ) 
    if cursor.fetchone(): 
        print(f"'{medicamento['nome']}' já foi marcado como tomado hoje.\n")
        conexao.close() 
        return 

    cursor.execute(
        "INSERT INTO registros_tomados (medicamento_id, data_tomado) VALUES (?, ?)", 
        (med_id, hoje), 
    )

    conexao.commit()
    conexao.close()

    print(f"\n '{medicamento['nome']}' marcado como tomado!\n")


def listar_todos_medicamentos() -> None: 
    conexao = get_conexao() 
    cursor = conexao.cursor() 

    cursor.execute(
        "SELECT id, nome, dosagem, horario, ativo FROM medicamentos ORDER BY horario"
    )
    medicamentos = cursor.fetchall() 
    conexao.close() 

    if not medicamentos: 
        print("\n Nenhum medicamento cadastrado \n")
        return 

    print("Todos medicamentos cadastrados:  ")
    print(f"  {'ID':<5} {'Horário':<10} {'Medicamento':<25} {'Dosagem':<20} {'Situação'}")
    print("  " + "─" * 70)

    for med in medicamentos:
        situacao = "🟢 Ativo" if med["ativo"] == 1 else "🔴 Inativo"
        print(
            f"  {med['id']:<5} {med['horario']:<10} {med['nome']:<25} {med['dosagem']:<20} {situacao}"
        )
 
    print()
 
 
def remover_medicamento() -> None:
    """
    Desativa um medicamento (soft delete).
    O registro permanece no banco para preservar o histórico.
    """
    listar_todos_medicamentos()
 
    conexao = get_conexao()
    cursor = conexao.cursor()
 
    try:
        med_id = int(input("🔢 Informe o ID do medicamento a remover: ").strip())
    except ValueError:
        print("⚠️  ID inválido. Digite apenas números.\n")
        conexao.close()
        return
 
    cursor.execute(
        "SELECT nome FROM medicamentos WHERE id = ? AND ativo = 1",
        (med_id,),
    )
    medicamento = cursor.fetchone()
 
    if not medicamento:
        print("⚠️  Medicamento não encontrado ou já está inativo.\n")
        conexao.close()
        return
 
    confirmacao = input(
        f"⚠️  Deseja remover '{medicamento['nome']}'? (s/n): "
    ).strip().lower()
 
    if confirmacao != "s":
        print("❌ Remoção cancelada.\n")
        conexao.close()
        return
 
    cursor.execute(
        "UPDATE medicamentos SET ativo = 0 WHERE id = ?",
        (med_id,),
    )
 
    conexao.commit()
    conexao.close()
 
    print(f"\n✅ '{medicamento['nome']}' removido com sucesso!\n")
 