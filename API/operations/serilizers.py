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

    is_active = fields.Boolean( 
        required=True,
        
        validate=ValidationHelper.must_not_be_blank
    )


class OperationSchema(ma.Schema):
    operation_id = fields.Integer()
    section_id = fields.Integer(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    operation_title = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    operation_description = fields.Str(
        required=True,
        validate=ValidationHelper.must_not_be_blank
    )
    is_active = fields.Boolean(
               
    )
    section = fields.Nested(SectionSchema)


