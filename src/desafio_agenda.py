from modules.menu import Menu
from modules.menu_functions import exibir_menu


def main() -> None:
    menu = Menu()
    while menu.status:
        try:
            exibir_menu()
            opcao = int(input("\nInsira a opção desejada: "))
            if 0 <= opcao <= 6:
                menu.status = menu.executar_opcao(opcao)
        except ValueError:
            menu.mensagem_valor_invalido()


if __name__ == "__main__":
    main()
