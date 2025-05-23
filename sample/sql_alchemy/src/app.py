from pathlib import Path

import bcrypt
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
from sample.sql_alchemy.src.models.user import User, UserRoles
from sample.sql_alchemy.src.modules.user_data_validator import (
    is_valid_cpf,
    is_valid_email,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
db_path = Path.cwd() / "sample" / "sql_alchemy" / "src" / "databases"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-alchemy"
)

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return (
                jsonify({"message": "Campos 'email' e 'password' são obrigatórios!"}),
                401,
            )

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(str.encode(password), user.password.encode()):
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso!"})
        return (
            jsonify({"message": "Usuário não encontrado ou credenciais inválidas!"}),
            401,
        )
    except Exception as e:
        current_app.logger.info(e)
        return jsonify({"message": "Erro interno no servidor."}), 500


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

        if current_user.role != UserRoles.ADMIN.value:
            return jsonify({"message": "Operação não permitida!"}), 403

        if missing_fields:
            return (
                jsonify(
                    {
                        "message": (
                            "Campos obrigatórios ausentes: "
                            + f"{', '.join(missing_fields)}"
                        )
                    }
                ),
                400,
            )

        if not is_valid_email(data["email"]):
            return (
                jsonify(
                    {"message": "E-mail inválido!", "data": {"email": data["email"]}}
                ),
                400,
            )

        if not is_valid_cpf(data["cpf"]):
            return (
                jsonify({"message": "CPF inválido!", "data": {"cpf": data["cpf"]}}),
                400,
            )

        unique_fields = get_user_unique_non_pk_columns(User)
        filters = [getattr(User, field) == data[field] for field in unique_fields]
        existing_user = User.query.filter(or_(*filters)).first()

        if not existing_user:
            user_data = {
                key: value
                for key, value in data.items()
                if key in User.__table__.columns.keys()
            }
            hashed_password = bcrypt.hashpw(
                str.encode(data["password"]), bcrypt.gensalt()
            )
            user_data["password"] = hashed_password
            user_data["role"] = UserRoles.USER.value

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
        current_app.logger.exception(f"Erro ao criar usuário: {e}")
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

        if user_id != current_user.id or current_user.role != UserRoles.ADMIN.value:
            return jsonify({"message": "Operação não permitida!"}), 403

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
                            + f"{', '.join(missing_fields)}"
                        )
                    }
                ),
                400,
            )

        if not is_valid_email(data["email"]):
            return (
                jsonify(
                    {"message": "E-mail inválido!", "data": {"email": data["email"]}}
                ),
                400,
            )

        if not is_valid_cpf(data["cpf"]):
            return (
                jsonify({"message": "CPF inválido!", "data": {"cpf": data["cpf"]}}),
                400,
            )

        unique_fields = get_user_unique_non_pk_columns(User)
        filters = [getattr(User, field) == data[field] for field in unique_fields]
        existing_data = User.query.filter(or_(*filters)).first()

        if existing_data and existing_data.id != user.id:
            return jsonify({"message": "Esses dados já estão sendo utilizados!"}), 400

        hashed_password = bcrypt.hashpw(str.encode(data["password"]), bcrypt.gensalt())
        data["password"] = hashed_password
        for key, value in data.items():
            if key in User.__table__.columns.keys():
                setattr(user, key, value)

        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso!"})

    except Exception as e:
        current_app.logger.exception(f"Erro ao atualizar usuário: {e}")
        return jsonify({"message": "Erro interno no servidor."}), 500


@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    try:
        user = User.query.get(user_id)

        if current_user.role != UserRoles.ADMIN.value:
            return jsonify({"message": "Operação não permitida!"}), 403

        if user_id == current_user.id:
            return jsonify({"message": "Deleção não permitida!"}), 403

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(
                {"mensagem": f"Usuário com id {user.id} deletado com sucesso!"}
            )
        return jsonify({"message": "Usuário não encontrado!"}), 404
    except Exception as e:
        current_app.logger.exception(f"Erro ao deletar usuário {user}: {e}")
        return jsonify({"message": "Erro interno no servidor."}), 500


def get_user_non_pk_columns(model):
    return [
        col.key
        for col in inspect(model).columns
        if not col.primary_key and col.key != "role"
    ]


def get_user_unique_non_pk_columns(model):
    return [
        col.key
        for col in inspect(model).columns
        if col.unique and not col.primary_key and col.key != "role"
    ]


def run_app(debug: bool = False):
    app.run(debug=debug)


if __name__ == "__main__":
    run_app(True)
