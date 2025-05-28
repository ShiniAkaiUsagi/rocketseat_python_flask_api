from enum import Enum

from marshmallow import Schema, fields, validate
from sqlalchemy import Boolean
from sqlalchemy import Enum as SqlEnum

from src.database import db


class MealTypes(str, Enum):
    BREAKFAST = "Café da manhã"
    LUNCH = "Almoço"
    SNACK = "Lanche"
    DINNER = "Janta"
    SUPPER = "Ceia"


class MealSchema(Schema):
    type = fields.String(
        required=True, validate=validate.OneOf([m.value for m in MealTypes])
    )
    description = fields.String(required=True, validate=validate.Length(max=200))
    timestamp = fields.String(required=True)
    is_diet_related = fields.Boolean(required=True)


class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(SqlEnum(MealTypes), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False)
    is_diet_related = db.Column(Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "timestamp": self.timestamp,
            "is_diet_related": self.is_diet_related,
        }
