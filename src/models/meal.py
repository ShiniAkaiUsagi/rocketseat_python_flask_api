from enum import Enum
from src.database import db
from marshmallow import Schema, fields, validate
from pydantic import BaseModel
from sqlalchemy import Enum as SqlEnum, Boolean


class MealTypes(str, Enum):
    BREAKFAST = "Café da manhã"
    BRUNCH = "Lanche da manhã"
    LUNCH = "Almoço"
    DINNER = "Janta"
    SUPPER = "Ceia"
    SNACK = "Lanche"


class MealSchema(Schema):
    type = fields.String(
        required=True,
        validate=validate.OneOf([meal.value for meal in MealTypes])
    )
    description = fields.String(required=True, validate=validate.Length(max=200))
    timestamp = fields.String(required=True)
    is_diet_related = fields.Boolean(required=True)


class MealCreate(BaseModel):
    type: MealTypes
    description: str
    timestamp: str
    is_diet_related: bool


class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(SqlEnum(MealTypes), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False)
    is_diet_related = db.Column(Boolean, nullable=False)
