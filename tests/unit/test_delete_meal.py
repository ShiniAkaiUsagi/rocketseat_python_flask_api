import pytest

from src.database import db


@pytest.mark.meal_delete
class TestDeleteMeal:
    def test_delete_meal_success(self, client, meal_registered):
        response = client.delete(f"/meal/{meal_registered.id}")
        assert response.status_code == 200
        assert "deletada com sucesso" in response.get_json()["message"]

    def test_delete_meal_not_found(self, client):
        response = client.delete("/meal/9999")
        assert response.status_code == 404
        assert "não encontrada" in response.get_json()["message"]

    def test_delete_meal_unhandled_exception(
        self, client, meal_registered, monkeypatch, dummy_bad_query
    ):
        monkeypatch.setattr(db.session, "commit", dummy_bad_query)
        response = client.delete(f"/meal/{meal_registered.id}")
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
