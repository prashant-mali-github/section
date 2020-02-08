from app import ma
from helpers.validators import ValidationHelper
from marshmallow import Schema, fields, pre_load, validate

class SectionSchema(ma.Schema):
    section_id = fields.Integer()

    section_title = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    section_description = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )

    is_active = fields.Boolean()


