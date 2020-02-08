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

class OperationSchema(ma.Schema):
    operation_id = fields.Integer()
    section_id = fields.Integer()
    operation_title = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    operation_description = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    is_active = fields.Boolean()


class RolesConfigSchema(ma.Schema):

    role_config_id = fields.Integer()
    role_id = fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    operation_id = fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    is_active = fields.Boolean()

    operation = fields.Nested(OperationSchema)
    role = fields.Nested(RolesSchema)