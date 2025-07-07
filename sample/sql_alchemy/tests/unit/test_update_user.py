import pytest
from faker import Faker
from faker.providers import person
from flask_login import login_user

from sample.sql_alchemy.src.database import db

faker = Faker("pt_BR")
faker.add_provider(person)


@pytest.mark.integration_update_user
class TestUpdateUser:
    """Testes para o endpoint /user/<id>, método PUT."""

    def test_update_user_as_admin_succeeded(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 200
        assert "Usuário atualizado com sucesso" in response.get_json()["message"]

    def test_update_self_user(self, client, regular_user, valid_payload):
        login_user(regular_user)
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 200
        assert "Usuário atualizado com sucesso" in response.get_json()["message"]

    def test_regular_user_tries_to_update_another(
        self, client, regular_user, admin_user, valid_payload
    ):
        login_user(regular_user)
        response = client.put(f"/user/{admin_user.id}", json=valid_payload)
        assert response.status_code == 403
        assert "Operação não permitida" in response.get_json()["message"]

    def test_update_user_not_found(self, client, admin_user, valid_payload):
        login_user(admin_user)
        response = client.put("/user/999999", json=valid_payload)
        assert response.status_code == 404
        assert "não encontrado" in response.get_json()["message"]

    def test_update_user_missing_fields(self, client, admin_user, regular_user):
        login_user(admin_user)
        payload = {"username": faker.first_name()}  # faltando campos obrigatórios
        response = client.put(f"/user/{regular_user.id}", json=payload)
        assert response.status_code == 400
        assert "Campos obrigatórios ausentes" in response.get_json()["message"]

    def test_update_user_invalid_email(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        valid_payload["email"] = "invalid_email"
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 400
        assert "E-mail inválido" in response.get_json()["message"]

    def test_update_user_invalid_cpf(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        valid_payload["cpf"] = "12345678900"  # CPF inválido
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 400
        assert "CPF inválido" in response.get_json()["message"]

    def test_update_user_invalid_cpf_less_digits(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        valid_payload["cpf"] = "123456789"
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 400
        assert "CPF inválido" in response.get_json()["message"]

    def test_update_user_duplicate_email(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        valid_payload["email"] = admin_user.email
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 400
        assert "já estão sendo utilizados" in response.get_json()["message"]

    def test_update_user_duplicate_cpf(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        valid_payload["cpf"] = admin_user.cpf
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 400
        assert "já estão sendo utilizados" in response.get_json()["message"]

    def test_update_user_duplicate_username(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        valid_payload["username"] = admin_user.username

        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 400
        assert "já estão sendo utilizados" in response.get_json()["message"]

    def test_update_user_with_invalid_field(
        self, client, admin_user, regular_user, valid_payload
    ):
        login_user(admin_user)
        invalid_payload = {**valid_payload, "invalid_field": "ignored_value"}
        response = client.put(f"/user/{regular_user.id}", json=invalid_payload)
        assert response.status_code == 400
        assert "campos não esperados" in response.get_json()["message"]

    def test_update_user_unhandled_exception(
        self,
        client,
        admin_user,
        regular_user,
        valid_payload,
        monkeypatch,
        dummy_bad_query,
    ):
        login_user(admin_user)
        monkeypatch.setattr(db.session, "commit", dummy_bad_query)
        response = client.put(f"/user/{regular_user.id}", json=valid_payload)
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
