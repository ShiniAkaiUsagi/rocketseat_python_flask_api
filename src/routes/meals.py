from flask import Blueprint, jsonify, request

from src.database import db
from src.models.meal import Meal
from src.modules.validation import get_required_columns, validate_fields

meal_bp = Blueprint("meals", __name__)


@meal_bp.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({"message": "Erro interno no servidor"}), 500


def validate_request_data(data, model):
    invalid_fields = validate_fields(data, model)
    if invalid_fields:
        return {
            "message": "Informado um ou mais campos não esperados!",
            "data": {"fields": ", ".join(invalid_fields)},
        }, 400

    required_fields = get_required_columns(model)
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            "message": "Campos obrigatórios ausentes!",
            "data": {"fields": ", ".join(missing_fields)},
        }, 400

    return None


@meal_bp.route("", methods=["POST"])
def register_meal():
    data = request.json
    validation_error = validate_request_data(data, Meal)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    new_meal = Meal(**data)
    db.session.add(new_meal)
    db.session.commit()
    return (
        jsonify(
            {"message": "Refeição registrada com sucesso!", "data": new_meal.to_dict()}
        ),
        201,
    )


@meal_bp.route("", methods=["GET"])
def list_meals():
    meals = Meal.query.all()
    meal_list = [meal.to_dict() for meal in meals]
    return jsonify({"meals": meal_list, "total": len(meal_list)})


@meal_bp.route("/<int:meal_id>", methods=["GET"])
def read_meal(meal_id):
    meal = db.session.get(Meal, meal_id)
    if meal:
        return jsonify({"message": "Refeição encontrada.", "data": meal.to_dict()})
    return jsonify({"message": "Refeição não encontrada!"}), 404


@meal_bp.route("/<int:meal_id>", methods=["PUT"])
def update_meal(meal_id):
    meal = db.session.get(Meal, meal_id)

    if not meal:
        return (jsonify({"message": f"Refeição com id {meal_id} não encontrada!"}), 404)

    data = request.json
    validation_error = validate_request_data(data, Meal)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]
    for key, value in data.items():
        setattr(meal, key, value)
    db.session.commit()
    return jsonify({"message": "Refeição atualizada com sucesso!"})


@meal_bp.route("/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    meal = db.session.get(Meal, meal_id)
    if not meal:
        return (
            jsonify({"message": f"Refeição com id {meal_id} não encontrada!"}),
            404,
        )

    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": f"Refeição com id {meal_id} deletada com sucesso!"})
