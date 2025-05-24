import bcrypt
import pytest
from sample.sql_alchemy.src.app import create_app
from sample.sql_alchemy.src.database import db
from sample.sql_alchemy.src.models.user import User, UserRoles

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        hashed_password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode('utf-8')
        admin_user = User(
            username="admin",
            cpf="12345678901",
            email="admin@admin.com",
            password=hashed_password,
            role=UserRoles.ADMIN.value
        )
        db.session.add(admin_user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
