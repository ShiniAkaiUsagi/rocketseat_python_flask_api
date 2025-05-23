from pathlib import Path

from flask import Flask, current_app, jsonify, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import inspect, or_

from sample.sql_alchemy.src.database import db
from sample.sql_alchemy.src.models.user import User
from sample.sql_alchemy.src.modules.user_data_validator import (
    is_valid_cpf,
    is_valid_email,
)

# from sample.sql_alchemy.src.models.user import User
# Hints: Organizar / ordenar os componentes do código pela taxa de atualização!

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
db_path = Path.cwd() / "sample" / "sql_alchemy" / "src" / "databases"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}/database.db"

# Doc Flask-Login
# https://flask-login.readthedocs.io/en/latest/

login_manager = LoginManager()

db.init_app(app)  # Session <- Conexão ativa

login_manager.init_app(app)

login_manager.login_view = "login"


# sql_alchemy record_queries
# https://flask-sqlalchemy.readthedocs.io/en/stable/api/#module-flask_sqlalchemy.record_queries


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return (
            jsonify({"message": "Campos 'email' e 'password' são obrigatórios.!"}),
            401,
        )

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        login_user(user)
        print(f"Usuário autenticado: {current_user.is_authenticated}")
        return jsonify({"message": "Autenticação realizada com sucesso!"})

    return jsonify({"message": "Usuário não encontrado ou credenciais inválidas!"}), 401


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Usuário deslogado com sucesso!"})


@app.route("/user", methods=["POST"])
@login_required
def create_user():
    try:
        data = request.json
        required_fields = get_user_non_pk_columns(User)

        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return (
                jsonify(
                    {
                        "message": (
                            "Campos obrigatórios ausentes: "
                            + f"{', '.join(missing_fields)})"
                        )
                    }
                ),
                400,
            )

        if not is_valid_email(data["email"]):
            return (
                jsonify(
                    {
                        "message": "E-mail inválido!",
                        "data": {"email": f"{data["email"]}"},
                    }
                )
            ), 400

        if not is_valid_cpf(data["cpf"]):
            return (
                jsonify({"message": "CPF inválido!", "data": {"cpf": f"{data["cpf"]}"}})
            ), 400

        unique_fields = get_user_unique_non_pk_columns(User)

        filters = [getattr(User, field) == data[field] for field in unique_fields]
        existing_user = User.query.filter(or_(*filters)).first()

        if not existing_user:
            user_data = {
                key: value
                for key, value in data.items()
                if key in User.__table__.columns.keys()
            }

            db.session.add(User(**user_data))
            db.session.commit()
            return jsonify({"message": "Usuário criado com sucesso!"}), 201

        return (
            jsonify(
                {"message": "Dados inválidos! Caso já tenha uma conta, faça login"}
            ),
            400,
        )

    except Exception as e:
        current_app.logger.exception(f"Erro ao criar usuário: {e}!")
        return jsonify({"message": "Erro interno no servidor."}), 500


@app.route("/user/<int:user_id>", methods=["GET"])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"mensagem": f"Usuário encontrado: {user.username}!"})
    return jsonify({"message": "Usuário não encontrado!"}), 404


@app.route("/user/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return (
                jsonify({"message": f"Usuário com id {user_id} não encontrado!"}),
                404,
            )

        data = request.json
        required_fields = get_user_non_pk_columns(User)

        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return (
                jsonify(
                    {
                        "message": (
                            "Campos obrigatórios ausentes: "
                            + f"{', '.join(missing_fields)})"
                        )
                    }
                ),
                400,
            )

        if not is_valid_email(data["email"]):
            return (
                jsonify(
                    {
                        "message": "E-mail inválido!",
                        "data": {"email": f"{data["email"]}"},
                    }
                )
            ), 400

        if not is_valid_cpf(data["cpf"]):
            return (
                jsonify({"message": "CPF inválido!", "data": {"cpf": f"{data["cpf"]}"}})
            ), 400

        unique_fields = get_user_unique_non_pk_columns(User)

        filters = [getattr(User, field) == data[field] for field in unique_fields]
        existing_data = User.query.filter(or_(*filters)).first()

        if not existing_data:
            user_data = {
                key: value
                for key, value in data.items()
                if key in User.__table__.columns.keys()
            }

            db.session.add(User(**user_data))
            db.session.commit()
            return jsonify({"message": "Usuário atualizado com sucesso!"}), 201

        return (
            jsonify({"message": "Esses dados não podem ser cadastrados!"}),
            400,
        )

    except Exception as e:
        current_app.logger.exception(f"Erro ao atualizar usuário: {e}!")
        return jsonify({"message": "Erro interno no servidor."}), 500


@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        if user_id == current_user.id:
            return jsonify({"mensagem": "Deleção não permitida!"}), 403

        db.session.delete(user)
        db.session.commit()
        return jsonify({"mensagem": f"Usuário com id {user.id} deletado com sucesso!"})
    return jsonify({"message": "Usuário não encontrado!"}), 404


def get_user_non_pk_columns(model):
    return [col.key for col in inspect(model).columns if not col.primary_key]


def get_user_unique_non_pk_columns(model):
    return [
        col.key for col in inspect(model).columns if col.unique and not col.primary_key
    ]


def run_app(debug: bool = False):
    app.run(debug=debug)


if __name__ == "__main__":
    run_app(True)
