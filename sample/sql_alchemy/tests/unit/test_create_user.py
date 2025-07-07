import pytest
from faker import Faker
from faker.providers import person
from flask_login import login_user

from sample.sql_alchemy.src.database import db
from sample.sql_alchemy.src.models.user import User, UserRoles

faker = Faker("pt_BR")
faker.add_provider(person)


@pytest.mark.integration_create_user
class TestCreateUser:
    """Testes para o endpoint /user, método POST."""

    @pytest.fixture
    def valid_payload(self):
        return {
            "username": faker.first_name(),
            "cpf": faker.cpf(),
            "email": faker.unique.email(),
            "password": "12345",
        }

    def test_create_user_succeeded(self, client, app, valid_payload, admin_user):
        with app.test_request_context():
            login_user(admin_user)

            response = client.post("/user", json=valid_payload)
            assert response.status_code == 201
            assert "Usuário criado com sucesso" in response.get_json()["message"]

            with app.app_context():
                user = User.query.filter_by(email=valid_payload["email"]).first()
                assert user is not None

    def test_create_user_forbidden_if_not_admin(
        self, client, valid_payload, mock_current_user
    ):
        mock_current_user(UserRoles.USER.value)

        response = client.post("/user", json=valid_payload)
        assert response.status_code == 403
        assert "Operação não permitida" in response.get_json()["message"]

    def test_create_user_missing_fields(self, client, mock_current_user):
        mock_current_user(UserRoles.ADMIN.value)

        payload = {"username": "incompleto"}
        response = client.post("/user", json=payload)
        assert response.status_code == 400
        assert "Campos obrigatórios ausentes" in response.get_json()["message"]

    def test_create_user_invalid_email(self, client, valid_payload, mock_current_user):
        mock_current_user(UserRoles.ADMIN.value)
        valid_payload["email"] = "email_invalido"

        response = client.post("/user", json=valid_payload)
        assert response.status_code == 400
        assert "E-mail inválido" in response.get_json()["message"]

    def test_create_user_invalid_cpf(self, client, valid_payload, mock_current_user):
        mock_current_user(UserRoles.ADMIN.value)
        valid_payload["cpf"] = "12345678900"  # CPF inválido

        response = client.post("/user", json=valid_payload)
        assert response.status_code == 400
        assert "CPF inválido" in response.get_json()["message"]

    def test_create_user_existing_email(
        self, client, regular_user, valid_payload, mock_current_user
    ):
        mock_current_user(UserRoles.ADMIN.value)
        valid_payload["email"] = regular_user.email
        response = client.post("/user", json=valid_payload)
        assert response.status_code == 400
        assert "Dados inválidos" in response.get_json()["message"]

    def test_create_user_existing_cpf(
        self, client, regular_user, valid_payload, mock_current_user
    ):
        mock_current_user(UserRoles.ADMIN.value)
        valid_payload["cpf"] = regular_user.cpf
        response = client.post("/user", json=valid_payload)
        assert response.status_code == 400
        assert "Dados inválidos" in response.get_json()["message"]

    def test_create_user_existing_username(
        self, client, regular_user, valid_payload, mock_current_user
    ):
        mock_current_user(UserRoles.ADMIN.value)
        valid_payload["username"] = regular_user.username
        response = client.post("/user", json=valid_payload)
        assert response.status_code == 400
        assert "Dados inválidos" in response.get_json()["message"]

    def test_create_user_with_invalid_field(
        self, client, mocker, valid_payload, mock_current_user
    ):
        mock_current_user(UserRoles.ADMIN.value)
        invalid_payload = {**valid_payload, "invalid_field": "ignored_value"}
        response = client.post("/user", json=invalid_payload)
        assert response.status_code == 400
        assert "campos não esperados" in response.get_json()["message"]

    def test_create_user_unhandled_exception(
        self, client, valid_payload, monkeypatch, mock_current_user, dummy_bad_query
    ):
        mock_current_user(UserRoles.ADMIN.value)

        monkeypatch.setattr(db.session, "commit", dummy_bad_query)

        response = client.post("/user", json=valid_payload)
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
