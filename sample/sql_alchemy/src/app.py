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

login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "admin123"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql:///root:admin123@127.0.0.1:3306/flask-crud"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.update(config or {})

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)

    @app.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json(silent=True) or {}

            required_fields = {
                "email": data.get("email"),
                "password": data.get("password"),
            }

            missing_fields = [
                field for field, value in required_fields.items() if not value
            ]

            if missing_fields:
                return (
                    jsonify(
                        {
                            "message": "Campos obrigatórios ausentes.",
                            "missing_fields": missing_fields,
                        }
                    ),
                    400,
                )

            email = required_fields["email"]
            password = required_fields["password"]

            user = User.query.filter_by(email=email).first()

            if user and bcrypt.checkpw(
                str.encode(password), user.password.encode("utf-8")
            ):
                login_user(user)
                user_loaded = load_user(user.id)
                return jsonify(
                    {
                        "message": "Autenticação realizada com sucesso!",
                        "data": {"id": f"{user_loaded.id}"},
                    }
                )

            return (
                jsonify(
                    {"message": "Usuário não encontrado ou credenciais inválidas!"}
                ),
                401,
            )

        except Exception as e:
            current_app.logger.info(e)
            return jsonify({"message": "Erro interno no servidor."}), 500

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Usuário deslogado com sucesso!"})

    @app.route("/user", methods=["POST"])
    @login_required
    def create_user():
        try:
            data = request.json
            invalid_fields = validate_fields(data, User)
            if invalid_fields:
                return (
                    jsonify(
                        {
                            "message": "Informado um ou mais campos não esperados!",
                            "data": {"fields": f"{', '.join(invalid_fields)}"},
                        }
                    ),
                    400,
                )

            required_fields = get_user_non_pk_columns(User)
            missing_fields = [field for field in required_fields if not data.get(field)]

            if current_user.role != UserRoles.ADMIN.value:
                return jsonify({"message": "Operação não permitida!"}), 403

            if missing_fields:
                return (
                    jsonify(
                        {
                            "message": "Campos obrigatórios ausentes!",
                            "data": {"fields": ", ".join(missing_fields)},
                        }
                    ),
                    400,
                )

            if not is_valid_email(data["email"]):
                return (
                    jsonify(
                        {
                            "message": "E-mail inválido!",
                            "data": {"email": data["email"]},
                        }
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
                user_data = {key: value for key, value in data.items()}
                hashed_password = bcrypt.hashpw(
                    str.encode(data["password"]), bcrypt.gensalt()
                )
                user_data["password"] = hashed_password.decode("utf-8")
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
        user = db.session.get(User, user_id)
        if user:
            return jsonify({"message": f"Usuário encontrado: {user.username}!"})
        return jsonify({"message": "Usuário não encontrado!"}), 404

    @app.route("/user/<int:user_id>", methods=["PUT"])
    @login_required
    def update_user(user_id):
        try:
            user = db.session.get(User, user_id)

            if (
                user_id != current_user.id
                and current_user.role != UserRoles.ADMIN.value
            ):
                return jsonify({"message": "Operação não permitida!"}), 403

            if not user:
                return (
                    jsonify({"message": f"Usuário com id {user_id} não encontrado!"}),
                    404,
                )

            data = request.json
            invalid_fields = validate_fields(data, User)
            if invalid_fields:
                return (
                    jsonify(
                        {
                            "message": "Informado um ou mais campos não esperados!",
                            "data": {"fields": f"{', '.join(invalid_fields)}"},
                        }
                    ),
                    400,
                )
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
                        {
                            "message": "E-mail inválido!",
                            "data": {"email": data["email"]},
                        }
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
                return (
                    jsonify({"message": "Esses dados já estão sendo utilizados!"}),
                    400,
                )

            hashed_password = bcrypt.hashpw(
                str.encode(data["password"]), bcrypt.gensalt()
            )
            data["password"] = hashed_password
            for key, value in data.items():
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
            user = db.session.get(User, user_id)

            if current_user.role != UserRoles.ADMIN.value:
                return jsonify({"message": "Operação não permitida!"}), 403

            if user_id == current_user.id:
                return jsonify({"message": "Deleção não permitida!"}), 403

            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify(
                    {"message": f"Usuário com id {user.id} deletado com sucesso!"}
                )
            return jsonify({"message": "Usuário não encontrado!"}), 404
        except Exception as e:
            current_app.logger.exception(
                f"Erro ao deletar usuário com id {user_id}: {e}"
            )
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

    def validate_fields(data: dict, model):
        """Valida se os campos de `data` existem nas colunas do `model`."""
        valid_fields = set(model.__table__.columns.keys())
        incoming_fields = set(data.keys())
        invalid_fields = incoming_fields - valid_fields
        return invalid_fields

    return app


def run_app(debug: bool = False):
    app = create_app()
    app.run(debug)


if __name__ == "__main__":
    run_app()
