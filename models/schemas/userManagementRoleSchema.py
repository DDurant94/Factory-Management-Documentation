from marshmallow import fields, validate
from schema import ma

class UserManagementRoleSchema(ma.Schema):
  id = fields.Integer(required=False)
  user_id = fields.Integer(required=True)
  role_id = fields.Integer(required=True)
  
user_management_schema = UserManagementRoleSchema()
users_management_schema = UserManagementRoleSchema(many=True)