from modules.menu_functions import MenuFunctions, mensagem_valor_invalido
from modules.menu_enum import MenuOpcao
from pathlib import Path

class Menu:
    BASE_DIR = Path.cwd()
    FILE_CONTATOS = BASE_DIR / "src" / "archive" / "lista_contatos.json"
    MSG_DESPEDIDA = "\nEncerrando aplicação. Até a próxima!"
    MSG_CONTINUAR = "\nDeseja continuar? (S/N): "
    MSG_OPCAO_INVALIDA = "\nOpção inválida!"


    def __init__(
        self,
        arquivo_contatos: str = FILE_CONTATOS,
    ):
        self.status: bool = True
        self.arquivo_contatos = arquivo_contatos
        self.menu_opcoes = MenuFunctions(self.arquivo_contatos)

    def deseja_continuar(self) -> bool:
        while True:
            resposta = input(self.MSG_CONTINUAR).strip().upper()
            if resposta == "S":
                return True
            elif resposta == "N":
                print(self.MSG_DESPEDIDA)
                return False
            mensagem_valor_invalido()

    def executar_opcao(self, opcao) -> None:
        self.menu_opcoes.carregar_contatos()
        match opcao:
            case MenuOpcao.LISTAR_CONTATOS.value:
                self.menu_opcoes.listar_contatos()
            case MenuOpcao.ADICIONAR_CONTATO.value:
                self.menu_opcoes.adicionar_contato()
            case MenuOpcao.EDITAR_CONTATO.value:
                self.menu_opcoes.editar_contato()
            case MenuOpcao.ALTERNAR_FAVORITO.value:
                self.menu_opcoes.alternar_favorito()
            case MenuOpcao.LISTAR_FAVORITOS.value:
                self.menu_opcoes.listar_contatos(filtrar_favoritos=True)
            case MenuOpcao.DELETAR_CONTATO.value:
                self.menu_opcoes.deletar_contato()
            case MenuOpcao.SAIR.value:
                print(self.MSG_DESPEDIDA)
                return False
            case _:
                print(self.MSG_OPCAO_INVALIDA)
                return True

        self.menu_opcoes.salvar_contatos()
        return self.deseja_continuar()
