from flask import request, jsonify
from caching import cache
from utils.util import token_required
from marshmallow import ValidationError

from models.schemas.rolesSchema import role_schema,roles_schema
from models.schemas.userManagementRoleSchema import user_management_schema,users_management_schema

from services import roleService

from utils.util import token_required,role_required

@token_required
@role_required('admin')
def save():
  try:
    role_data = role_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    role_save = roleService.save(role_data)
    return role_schema.jsonify(role_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
@token_required
@role_required('admin')
def find_all():
  roles = roleService.find_all()
  return roles_schema.jsonify(roles), 200
    