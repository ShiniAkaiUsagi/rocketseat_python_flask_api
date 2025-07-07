import pytest
from faker import Faker
from faker.providers import person
from flask_login import login_user

from sample.sql_alchemy.src.database import db

faker = Faker("pt_BR")
faker.add_provider(person)


@pytest.mark.integration_delete_user
class TestDeleteUser:
    """Testes para o endpoint /user, método DELETE."""

    def test_delete_user_by_admin(self, client, admin_user, regular_user):
        login_user(admin_user)
        response = client.delete(f"/user/{regular_user.id}")
        assert response.status_code == 200
        assert (
            f"Usuário com id {regular_user.id} deletado com sucesso!"
            in response.get_json()["message"]
        )

    def test_admin_cannot_delete_self(self, client, admin_user):
        login_user(admin_user)
        response = client.delete(f"/user/{admin_user.id}")
        assert response.status_code == 403
        assert "Deleção não permitida" in response.get_json()["message"]

    def test_non_admin_cannot_delete_user(self, client, regular_user, admin_user):
        login_user(regular_user)
        response = client.delete(f"/user/{admin_user.id}")
        assert response.status_code == 403
        assert "Operação não permitida" in response.get_json()["message"]

    def test_delete_nonexistent_user(self, client, admin_user):
        login_user(admin_user)
        response = client.delete("/user/999999")
        assert response.status_code == 404
        assert "Usuário não encontrado" in response.get_json()["message"]

    def test_delete_user_unhandled_exception(
        self, monkeypatch, client, admin_user, regular_user, dummy_bad_query
    ):
        login_user(admin_user)
        monkeypatch.setattr(db.session, "commit", dummy_bad_query)
        response = client.delete(f"/user/{regular_user.id}")
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
