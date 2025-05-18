# RocketSeat - Desafio 01 - Agenda

Projeto criado como forma de fixar e avaliar os conhecimentos obtidos no módulo 1: "Introdução ao Python".
O [Desafio proposto](Desafio01.txt) foi criar uma agenda de contatos com algumas funcionalidades básicas.

### Funcionalidades

- Adicionar, editar e remover contatos;
- Favoritar e desfavoritar contatos; e
- Listar Contatos

## Requisitos

- [Python 3.13](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/nome-do-projeto.git

# 2. Acesse a pasta do projeto
cd nome-do-projeto

# 3. Execute o script de build para preparar as ferramentas e ambiente
sh scripts/build.sh

# O script executa:
# python.exe -m pip install --upgrade pip
# pip install -U poetry
# poetry install
# poetry run pre-commit run
```

## Executando a aplicação
```bash
# Para executar o código da Agenda, basta utilizar o comando abaixo:
poetry run python src/desafio_agenda.py
```
