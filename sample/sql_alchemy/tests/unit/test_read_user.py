import pytest
from flask_login import login_user


@pytest.mark.integration_read_user
class TestReadUser:
    """Testes para o endpoint /read_user."""

    def test_read_user_found(self, client, admin_user, regular_user):
        login_user(admin_user)
        response = client.get(f"/user/{regular_user.id}")
        assert response.status_code == 200
        assert "Usuário encontrado" in response.get_json()["message"]

    def test_read_user_not_found(self, client, admin_user):
        login_user(admin_user)
        response = client.get("/user/9999")
        assert response.status_code == 404
        assert "Usuário não encontrado" in response.get_json()["message"]
