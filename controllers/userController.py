from flask import request, jsonify
from caching import cache
from utils.util import token_required
from marshmallow import ValidationError

from services import userService

from models.schemas.userSchema import user_schema,users_schema

from utils.util import token_required,role_required


def save():
  try:
    user_data = user_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    user_save = userService.save(user_data)
    return user_schema.jsonify(user_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
  
  
@token_required
@role_required('admin')
def find_all():
  users = userService.find_all()
  return users_schema.jsonify(users),200

def login():
  user = request.json
  user = userService.login_user(user['username'], user['password'])
  if user:
    return jsonify(user),200
  else:
    resp={
      "status":"Error",
      "message": "User does not exist"
    }
    return jsonify(resp), 400