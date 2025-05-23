from pathlib import Path

from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from sample.sql_alchemy.src.database import db
from sample.sql_alchemy.src.models.user import User

# from sample.sql_alchemy.src.models.user import User
# Hints: Organizar / ordenar os componentes do código pela taxa de atualização!

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
db_path = Path.cwd() / "sample" / "sql_alchemy" / "src" / "databases"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}/database.db"

PASSWORD = 123
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
    print(password)
    if not email or not password:
        return (
            jsonify({"message": "Campos 'email' e 'password' são obrigatórios.!"}),
            401,
        )

    if email and password:
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


def run_app(debug: bool = False):
    app.run(debug=debug)


if __name__ == "__main__":
    run_app(True)
