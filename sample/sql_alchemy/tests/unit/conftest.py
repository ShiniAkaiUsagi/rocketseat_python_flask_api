import bcrypt
import pytest
from faker import Faker
from faker.providers import person

from sample.sql_alchemy.src.app import create_app
from sample.sql_alchemy.src.database import db
from sample.sql_alchemy.src.models.user import User, UserRoles

faker = Faker("pt_BR")
faker.add_provider(person)


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        hashed_password = bcrypt.hashpw(b"12345", bcrypt.gensalt()).decode("utf-8")
        admin = User(
            username="admin",
            cpf=faker.cpf(),
            email="admin@admin.com",
            password=hashed_password,
            role=UserRoles.ADMIN.value,
        )
        user = User(
            username="regular_user",
            cpf=faker.cpf(),
            email="user@user.com",
            password=hashed_password,
            role=UserRoles.USER.value,
        )
        db.session.add_all([admin, user])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def admin_user(app):
    with app.app_context():
        return User.query.filter_by(email="admin@admin.com").first()


@pytest.fixture
def regular_user(app):
    with app.app_context():
        return User.query.filter_by(email="user@user.com").first()


@pytest.fixture
def client(app):
    return app.test_client()


class DummyQuery:
    def first(self):
        raise RuntimeError("boom")


@pytest.fixture
def dummy_bad_query():
    """Fornece um objeto que sempre lança na .first()."""
    return DummyQuery()


@pytest.fixture
def mock_current_user(mocker):
    def _mock(role):
        """Mocka current_user com o papel desejado."""
        user = User()
        user.id = 1  # ou qualquer valor necessário para os testes
        user.role = role
        mocker.patch("flask_login.utils._get_user", return_value=user)
        return user

    return _mock


@pytest.fixture
def valid_payload():
    return {
        "username": faker.first_name(),
        "cpf": faker.cpf(),
        "email": faker.unique.email(),
        "password": "12345",
    }
