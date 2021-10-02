from marshmallow import Schema
from webargs import fields, validate


class IntParamFromOneToFifty(Schema):
    count = fields.Integer(
        required=False,
        missing=10,
        validate=[validate.Range(min=1, max=50)],
    )
