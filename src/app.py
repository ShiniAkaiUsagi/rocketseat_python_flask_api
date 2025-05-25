from flask import Flask, current_app, jsonify, request
from sqlalchemy import inspect, or_

from src.database import db
from src.models.meal import Meal


def create_app(config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "admin123"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql:///root:admin123@127.0.0.1:3306/flask-crud"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.update(config or {})

    db.init_app(app)

    return app


def run_app(debug: bool = False):
    app = create_app()
    app.run(debug)


if __name__ == "__main__":
    run_app()
