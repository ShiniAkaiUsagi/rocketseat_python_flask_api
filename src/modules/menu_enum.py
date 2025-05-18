from enum import Enum


class MenuOpcao(Enum):
    LISTAR_CONTATOS = 1
    ADICIONAR_CONTATO = 2
    EDITAR_CONTATO = 3
    ALTERNAR_FAVORITO = 4
    LISTAR_FAVORITOS = 5
    DELETAR_CONTATO = 6
    SAIR = 0