from marshmallow import fields, validate
from schema import ma

class RoleSchema(ma.Schema):
  id = fields.Integer(required=False)
  role_name = fields.String(required=True, validate=validate.Length(min=1))
  
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)