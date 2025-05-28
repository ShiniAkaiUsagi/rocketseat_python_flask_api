import pytest

from src.database import db


@pytest.mark.meal_update
class TestUpdateMeal:
    def test_update_meal_success(self, client, meal_registered):
        meal = {
            "type": "Ceia",
            "description": "Iogurte natural",
            "timestamp": "2025-05-27 22:00:00",
            "is_diet_related": True,
        }
        response = client.put(f"/meal/{meal_registered.id}", json=meal)

        assert response.status_code == 200
        assert "atualizada com sucesso" in response.get_json()["message"]

    def test_update_meal_not_found(self, client):
        meal = {
            "type": "Ceia",
            "description": "Iogurte",
            "timestamp": "2025-05-27 22:00:00",
            "is_diet_related": True,
        }
        response = client.put("/meal/9999", json=meal)
        assert response.status_code == 404
        assert "não encontrada" in response.get_json()["message"]

    def test_update_meal_invalid_field(self, client, meal_registered):
        meal = {
            "description": "Iogurte",
            "timestamp": "2025-05-27 22:00:00",
            "is_diet_related": True,
            "invalid": "ops",
        }
        response = client.put(f"/meal/{meal_registered.id}", json=meal)

        assert response.status_code == 400
        assert "campos não esperados" in response.get_json()["message"]

    def test_update_meal_unhandled_exception(
        self, client, meal_registered, monkeypatch, dummy_bad_query, valid_payload
    ):
        monkeypatch.setattr(db.session, "commit", dummy_bad_query)
        response = client.put(f"/meal/{meal_registered.id}", json=valid_payload)
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
