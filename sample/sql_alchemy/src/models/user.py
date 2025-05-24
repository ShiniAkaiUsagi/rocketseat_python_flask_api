from enum import Enum

from flask_login import UserMixin

from sample.sql_alchemy.src.database import db

# PalletsProject:
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/#defining-models


class UserRoles(Enum):
    USER = "user"
    ADMIN = "admin"


# Herdamos os recursos para autenticação da classe parent UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False, default=UserRoles.USER.value)
