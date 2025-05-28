import pytest

from src.database import db


@pytest.mark.meal_post
class TestCreateMeal:
    def test_register_meal_success(self, client, valid_payload):
        response = client.post("/meal", json=valid_payload)
        assert response.status_code == 201
        assert response.get_json()["message"] == "Refeição registrada com sucesso!"

    def test_register_meal_missing_field(self, client, valid_payload):
        valid_payload.pop(next(iter(valid_payload)))
        response = client.post("/meal", json=valid_payload)
        assert response.status_code == 400
        assert "Campos obrigatórios ausentes" in response.get_json()["message"]

    def test_register_meal_invalid_field(self, client, valid_payload):
        valid_payload["extra_field"] = "não deveria estar aqui"
        response = client.post("/meal", json=valid_payload)
        assert response.status_code == 400
        assert "campos não esperados" in response.get_json()["message"]

    def test_register_meal_unhandled_exception(
        self, client, monkeypatch, dummy_bad_query, valid_payload
    ):
        monkeypatch.setattr(db.session, "commit", dummy_bad_query)
        response = client.post("/meal", json=valid_payload)
        assert response.status_code == 500
        assert "Erro interno no servidor" in response.get_json()["message"]
