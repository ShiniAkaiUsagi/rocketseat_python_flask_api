# RocketSeat - Desafio 01 - Agenda

Projeto criado como forma de fixar e avaliar os conhecimentos obtidos no módulo 2: "Desenvolvimento de APIs com Flask".
O [Desafio proposto](Desafio02.txt) ...

### Funcionalidades


## Requisitos

- [Python 3.13](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/ShiniAkaiUsagi/rocketseat_python_flask_api.git

# 2. Acesse a pasta do projeto
cd rocketseat_python_python_flask_api

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
# Para executar os testes unitários da API, já configurado no pyproject.toml:
poetry run pytest

# Para 'ligar' o API Server e poder enviar requisições da máquina:
# para a api crud tarefas
PYTHONPATH=. poetry run python sample/crud_tarefas/src/app.py
# ou para api em conjunto com a sql_alchemy
PYTHONPATH=. poetry run python sample/sql_alchemy/src/app.py

# Para o sample do SQL Alchemy
# Para acessar o flask shell:
FLASK_APP=sample.sql_alchemy.src.app flask shell

db.session  # exibir a sessão
db.create_all()  # criar as tabelas utilizadas em código

#Para criar um usuario no database criado:
user = User(username="admin", cpf="00000000001", email="admin@admin.com", password="123")
user    # verifica se o objeto foi criado
user.username # loga o valor da chave username

db.session.add(user)    # adiciona o user no banco, nessa sessão
db.session.commit()  # Salva as alterações na sessão:
exit()
```
