from enum import Enum

from flask_login import UserMixin

from sample.sql_alchemy.src.database import db

# PalletsProject:
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/#defining-models
from marshmallow import Schema, fields, validate
from pydantic import BaseModel

from sqlalchemy import Enum as SqlEnum


class UserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserSchema(Schema):
    username = fields.String(required=True)
    cpf = fields.String(required=True, validate=validate.Length(equal=11))
    email = fields.Email(required=True)
    password = fields.String(required=True)
    role = fields.String(
        required=True,
        validate=validate.OneOf([role.value for role in UserRoles])
    )


class UserCreate(BaseModel):
    username: str
    cpf: str
    email: str
    password: str
    role: UserRoles


# Herdamos os recursos para autenticação da classe parent UserMixin
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(SqlEnum(UserRoles), nullable=False, default=UserRoles.USER)
