from marshmallow import fields, validate
from schema import ma

class UserSchema(ma.Schema):
  id = fields.Integer(required=False)
  username = fields.String(required=True,validate=validate.Length(min=5,max=20))
  password = fields.String(required=True,validate=validate.Length(min=8,max=20))
  role = fields.String(required=False,validate=validate.Length(min=2))
  
  
user_schema = UserSchema()
users_schema = UserSchema(many=True)