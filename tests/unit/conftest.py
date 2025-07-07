import random
from datetime import datetime, timedelta

import pytest

from src.app import create_app
from src.database import db
from src.models.meal import Meal, MealTypes


@pytest.fixture(scope="session")
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
        db.session.add_all(
            [
                Meal(
                    type="Almoço",
                    description="Frango com arroz",
                    timestamp="2025-05-27 12:00:00",
                    is_diet_related=True,
                ),
                Meal(
                    type="Lanche",
                    description="Pastel",
                    timestamp="2025-05-27 16:30:00",
                    is_diet_related=False,
                ),
            ]
        )
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def valid_payload(gerar_refeicao):
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    timestamp = datetime.fromtimestamp(
        random.uniform(start_date.timestamp(), end_date.timestamp())
    )

    return {
        "type": random.choice(list(MealTypes)),
        "description": gerar_refeicao,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "is_diet_related": random.choice([True, False]),
    }


@pytest.fixture
def meal_registered(app):
    with app.app_context():
        return Meal.query.first()


@pytest.fixture
def gerar_refeicao():
    tipos_refeicao = ["café da manhã", "almoço", "jantar", "lanche", "sobremesa"]
    refeicoes_simples = {
        "café da manhã": [
            "pão com manteiga",
            "tapioca",
            "café com leite",
            "frutas",
        ],
        "almoço": ["arroz com feijão", "macarrão", "frango assado", "salada"],
        "jantar": ["sopa", "torta", "wrap", "pizza"],
        "lanche": ["pão de queijo", "barra de cereal", "biscoito", "suco"],
        "sobremesa": ["pudim", "sorvete", "brigadeiro", "fruta"],
    }
    tipo = random.choice(tipos_refeicao)
    return random.choice(refeicoes_simples[tipo])


class DummyQuery:
    def first(self):
        raise RuntimeError("boom")


@pytest.fixture
def dummy_bad_query():
    """Fornece um objeto que sempre lança na .first()."""
    return DummyQuery()
