from flask import request, jsonify
from marshmallow import ValidationError
from caching import cache
from database import db

from models.schemas.orderSchema import order_schema,orders_schema

from services import orderService

from utils.util import token_required,role_required

def save():
  try:
    order_data = order_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  
  try:
    order_save = orderService.save(order_data)
    return order_schema.jsonify(order_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400

@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
  page = request.args.get('page',1,type=int)
  per_page=request.args.get('per_page',10,type=int)
  return orders_schema.jsonify(orderService.find_all(page=page,per_page=per_page)),200