from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask, test_config: dict = None):
    """Inicializa o app com configuração normal ou de teste."""
    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "mysql+pymysql://root:123456@localhost:3306/sql_alchemy_db"
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
