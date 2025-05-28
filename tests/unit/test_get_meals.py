import pytest

from src.database import db


@pytest.mark.meal_get
class TestGetMeals:
    def test_get_all_meals(self, client):
        response = client.get("/meal")
        assert response.status_code == 200
        assert isinstance(response.json["meals"], list)

    def test_get_meal_by_id_success(self, client, meal_registered):
        response = client.get(f"/meal/{meal_registered.id}")
        assert response.status_code == 200
        assert response.get_json()["data"]["description"] == meal_registered.description

    def test_get_meal_by_id_not_found(self, client):
        response = client.get("/meal/9999")
        assert response.status_code == 404
        assert "não encontrada" in response.get_json()["message"]

    def test_get_meal_unhandled_exception(
        self, client, meal_registered, monkeypatch, dummy_bad_query
    ):
        monkeypatch.setattr(db.session, "get", dummy_bad_query)
        response = client.get(f"/meal/{meal_registered.id}")
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
