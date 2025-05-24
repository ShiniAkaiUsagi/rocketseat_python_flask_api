# RocketSeat - Desafio 01 - Agenda

Projeto criado como forma de fixar e avaliar os conhecimentos obtidos no módulo 2: "Desenvolvimento de APIs com Flask".
O [Desafio proposto](Desafio02.txt) ...

### Funcionalidades


## Requisitos

- [Python 3.13](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://docs.docker.com/desktop/)

#### VSCode Extensions recomendadas:
- SQLite Viewer
- MySQL (database-client.com)

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
# poetry self add poetry-plugin-export
# poetry self update
# poetry update
# poetry run pre-commit run
# # E para instalar as dependências na máquina local, além do ambiente virtual:
# poetry export --without-hashes --format=requirements.txt -o requirements.txt
# pip install -U -r requirements.txt

```

### Para executar os testes unitários de todos os projetos:
```bash
PYTHONPATH=. poetry run pytest
```

### Passos iniciais para o SubProjeto task-manager
```bash

# Para 'ligar' o API Server e poder enviar requisições da máquina:
PYTHONPATH=. poetry run python sample/crud_tarefas/src/app.py
```
`


### Passos iniciais para o SubProjeto sql_alchemy
```bash
# Terminal 1: Inicie a aplicação
PYTHONPATH=. poetry run python sample/sql_alchemy/src/app.py
# Terminal 2: Conecte o docker para nos conectarmos ao banco de dados
docker-compose up
# Terminal 3: Crie o database e crie os 2 usuários iniciais como teste
db.drop_all()
db.create_all()

user = User(username="admin", cpf="00000000001", email="admin@admin.com", password="12345", role="admin")
db.session.add(user)

user = User(username="notadmin", cpf="00000000002", email="admin2@admin.com", password="12345", role="user")
db.session.add(user)

db.session.commit()
exit()
```

##### Alternando bancos de dados (MySQL vs SQLite)
No arquivo da aplicação (app.py), basta escolher uma das conexões abaixo.
Para isso, 'comente' ou exclua no arquivo app.py a linha que não irá utilizar:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/flask-crud'
```