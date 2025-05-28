from sqlalchemy import inspect


def validate_fields(data: dict, model):
    valid_fields = set(model.__table__.columns.keys())
    incoming_fields = set(data.keys())
    return incoming_fields - valid_fields


def get_required_columns(model):
    return [col.key for col in inspect(model).columns if not col.primary_key]
