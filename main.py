from database import inicializar_banco

from medicamentos import (
    cadastrar_medicamento,
    listar_medicamentos_do_dia,
    marcar_como_tomado,
    listar_todos_medicamentos,
    remover_medicamento,
    consultar_medicamento_com_api
)

BANNER = """
╔══════════════════════════════════════════════════╗
║         💊 CONTROLE DE MEDICAMENTOS              ║
║         Sua rotina de saúde em dia!              ║
╚══════════════════════════════════════════════════╝
"""


MENU = """
┌──────────────────────────────────────────────────┐
│                   MENU PRINCIPAL                 │
├──────────────────────────────────────────────────┤
│  1. Cadastrar Medicamento                        │
│  2. Ver Medicamentos do Dia                      │
│  3. Marcar Medicamento como Tomado               │
│  4. Ver Todos os Medicamentos Cadastrados        │
│  5. Remover Medicamento                          │
│  6. Consultar Informações de Medicamento         │
│  0. Sair                                         │
└──────────────────────────────────────────────────┘
"""


def exibir_banner():
    print(BANNER)


def exibir_menu():
    print(MENU)

    opcao = input("Escolha uma opção: ").strip()

    return opcao


def executar_opcao(opcao: str) -> bool:
    if opcao == "1":
        print("\n── Cadastrar Medicamento ──")
        cadastrar_medicamento()

    elif opcao == "2":
        print("\n── Medicamentos do Dia ──")
        listar_medicamentos_do_dia()

    elif opcao == "3":
        print("\n── Marcar Medicamento como Tomado ──")
        marcar_como_tomado()

    elif opcao == "4":
        print("\n── Todos os Medicamentos ──")
        listar_todos_medicamentos()

    elif opcao == "5":
        print("\n── Remover Medicamento ──")
        remover_medicamento()

    elif opcao == "6":
        print("\n── Consultar Medicamento via Groq API ──")
        consultar_medicamento_com_api()

    elif opcao == "0":
        print("\n Encerrando o sistema.")

        return False

    else:
        print("\n Opção inválida! Por favor, escolha uma opção")
        print(" disponível no menu")

    return True


def main():
    inicializar_banco()
    exibir_banner()

    continuar = True
    while continuar:
        opcao = exibir_menu()
        continuar = executar_opcao(opcao)


if __name__ == "__main__":
    main()
