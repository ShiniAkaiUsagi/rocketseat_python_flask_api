import json

from modules.menu_enum import MenuOpcao


def exibir_menu():
    print("*** Agenda de Contatos ***\n")
    for opcao in MenuOpcao:
        print(f"{opcao.value}. {opcao.name.replace('_', ' ').capitalize()}")


def mensagem_contato_nao_encontrado() -> None:
    print("Contato não encontrado!")


def mensagem_valor_invalido() -> None:
    print("Valor inválido!")


class MenuFunctions:
    def __init__(self, arquivo_contatos: str = None):
        self.arquivo_contatos = arquivo_contatos
        self.lista_contatos = self.carregar_contatos()

    def carregar_contatos(self) -> list:
        try:
            with open(self.arquivo_contatos, "r", encoding="utf-8") as arquivo:
                print("\nLista de contatos carregada/atualizada com sucesso!")
                self.lista_contatos = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            self.lista_contatos = []

    def salvar_contatos(self) -> None:
        with open(self.arquivo_contatos, "w", encoding="utf-8") as arquivo:
            json.dump(self.lista_contatos, arquivo, indent=4, ensure_ascii=False)

    def solicitar_indice_contato(self) -> int | None:
        try:
            indice = int(input("\nDigite o ID do contato: "))
            indice_real = indice - 1
            if 0 <= indice_real < len(self.lista_contatos):
                return indice_real
            else:
                mensagem_contato_nao_encontrado()
        except ValueError:
            mensagem_valor_invalido()
        return None

    def exibir_contato(self, index: int, contato: dict) -> None:
        print(f"- Contato {index}")
        print(f"Nome: {contato['nome'].title()}")
        print(f"Email: {contato['email']}")
        print(f"Telefone: {contato['telefone']}")
        print(f"Favorito: {'Sim' if contato['favorito'] else 'Não'}\n")

    def listar_contatos(self, filtrar_favoritos: bool = False) -> bool:
        print("\n*** Listando contatos salvos: ***\n")

        if filtrar_favoritos:
            print("\nFiltrando contatos favoritos...")
            contatos_filtrados = [
                (index, contato)
                for index, contato in enumerate(self.lista_contatos, start=1)
                if contato["favorito"]
            ]
        else:
            contatos_filtrados = list(enumerate(self.lista_contatos, start=1))

        if not contatos_filtrados:
            mensagem_contato_nao_encontrado()
            return False

        print(f"\nTotal de contatos encontrados: {len(contatos_filtrados)}\n")
        for index, contato in contatos_filtrados:
            self.exibir_contato(index, contato)

        return True

    def adicionar_contato(self) -> None:
        print("\n*** Adicionando contato na Agenda: ***\n")
        nome = input("Nome: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("Email: ").strip()
        favorito = input("Marcar como favorito? (S/N): ")
        novo_contato = {
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "favorito": True if favorito.upper() == "S" else False,
        }
        self.lista_contatos.append(novo_contato)
        self.salvar_contatos()
        print("Contato adicionado!")

    def obter_contato(self, indice: int) -> dict | None:
        return (
            self.lista_contatos[indice]
            if 0 <= indice < len(self.lista_contatos)
            else None
        )

    def atualizar_contato_por_indice(
        self, indice, nome=None, telefone=None, email=None, favorito=None
    ) -> bool:
        contato = self.obter_contato(indice)
        if not contato:
            return False

        contato["nome"] = nome if nome else contato["nome"]
        contato["telefone"] = telefone if telefone else contato["telefone"]
        contato["email"] = email if email else contato["email"]
        contato["favorito"] = favorito if favorito is not None else contato["favorito"]
        return True

    def editar_contato(self) -> bool:
        status_listagem = self.listar_contatos()
        if not status_listagem:
            return False

        try:
            indice_real = self.solicitar_indice_contato()
            if indice_real is None:
                return False

            contato = self.obter_contato(indice_real)

            if contato:
                print("\nDeixe o campo vazio para manter o valor atual.")
                nome = input(f"Novo nome ({contato['nome'].title()}): ").strip()
                telefone = input(f"Novo telefone ({contato['telefone']}): ").strip()
                email = input(f"Novo email ({contato['email']}): ").strip()

                self.atualizar_contato_por_indice(indice_real, nome, telefone, email)
                self.salvar_contatos()
                print("\nContato atualizado com sucesso!")
                return True
            else:
                mensagem_contato_nao_encontrado()
                return False
        except ValueError:
            mensagem_valor_invalido()
            return False

    def alternar_favorito(self) -> bool:
        status_listagem = self.listar_contatos()
        if not status_listagem:
            return False

        indice_real = self.solicitar_indice_contato()
        if indice_real is None:
            return False

        contato = self.obter_contato(indice_real)
        if not contato:
            mensagem_contato_nao_encontrado()
            return False

        acao = "desfavoritar" if contato["favorito"] else "favoritar"
        while True:
            escolha = input(f"Deseja {acao} este contato? (S/N): ").strip().upper()

            if escolha == "S":
                contato["favorito"] = not contato["favorito"]
                self.atualizar_contato_por_indice(
                    indice_real, favorito=contato["favorito"]
                )
                self.salvar_contatos()
                print("\nContato atualizado com sucesso!")
                return True
            elif escolha == "N":
                print("Nenhuma alteração feita.")
                return False
            mensagem_valor_invalido()

    def deletar_contato(self) -> bool:
        status_listagem = self.listar_contatos()
        if not status_listagem:
            return False

        indice_real = self.solicitar_indice_contato()
        if indice_real is None:
            return False

        self.lista_contatos.pop(indice_real)
        self.salvar_contatos()
        print("\nContato deletado com sucesso!")
        return True
