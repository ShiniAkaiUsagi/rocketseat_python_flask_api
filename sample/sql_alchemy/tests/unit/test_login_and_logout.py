import pytest

from sample.sql_alchemy.src.database import db


@pytest.mark.integration_login
class TestLogin:
    """Testes para o endpoint /login."""

    @pytest.mark.parametrize(
        "email,password,expected_status,expected_message",
        [
            ("admin@admin.com", "12345", 200, "Autenticação realizada com sucesso!"),
            ("wrong@admin.com", "12345", 401, "credenciais inválidas"),
            ("admin@admin.com", "wrongpass", 401, "credenciais inválidas"),
            ("", "12345", 400, "Campos obrigatórios ausentes"),
            ("admin@admin.com", "", 400, "Campos obrigatórios ausentes"),
        ],
        ids=[
            "login_ok",
            "login_fail_invalid_email",
            "login_fail_invalid_password",
            "login_fail_empty_email",
            "login_fail_empty_password",
        ],
    )
    def test_login_various(
        self, client, email, password, expected_status, expected_message
    ):
        response = client.post("/login", json={"email": email, "password": password})
        assert response.status_code == expected_status
        print(response.get_json())
        assert expected_message in response.get_json()["message"]

    def test_login_missing_field_email(self, client):
        response = client.post("/login", json={"password": "12345"})
        assert response.status_code == 400
        assert "Campos obrigatórios ausentes" in response.get_json()["message"]

    def test_login_missing_field_passwords(self, client):
        response = client.post("/login", json={"email": "admin@admin.com"})
        assert response.status_code == 400
        assert "Campos obrigatórios ausentes" in response.get_json()["message"]

    def test_login_internal_error(self, client, monkeypatch, dummy_bad_query):
        monkeypatch.setattr(db.session, "get", dummy_bad_query)

        response = client.post(
            "/login", json={"email": "admin@admin.com", "password": "12345"}
        )
        assert response.status_code == 500
        assert response.get_json()["message"] == "Erro interno no servidor."


@pytest.mark.integration_logout
class TestLogout:
    """Testes para o endpoint /logout."""

    def test_logout_succeeded(self, client):
        """Testa o logout por um usuário logado"""
        with client:
            login_response = client.post(
                "/login",
                json={"email": "admin@admin.com", "password": "12345"},
            )
            assert login_response.status_code == 200

            response = client.post("/logout")
            assert response.status_code == 200
            assert response.get_json()["message"] == "Usuário deslogado com sucesso!"

    def test_logout_without_login(self, client):
        """Testa o logout por um usuário deslogado"""
        response = client.post("/logout")
        assert response.status_code == 302
