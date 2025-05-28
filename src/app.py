from flask import Flask

from src.database import init_app
from src.routes.meals import meal_bp


def create_app(config: dict = None):
    app = Flask(__name__)

    default_config = {
        "SECRET_KEY": "admin123",
        "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://root:admin123@localhost:3306/sql_alchemy_db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    if config:
        default_config.update(config)

    app.config.update(default_config)

    init_app(app)
    app.register_blueprint(meal_bp, url_prefix="/meal")

    return app


def run_app(debug: bool = False):
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
