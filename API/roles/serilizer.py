from app import ma
from helpers.validators import ValidationHelper
from marshmallow import Schema, fields, pre_load, validate

class RolesSchema(ma.Schema):
    role_id = fields.Integer()

    role_title = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    role_description = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

    is_active = fields.Boolean()


