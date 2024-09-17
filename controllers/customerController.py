from flask import request, jsonify
from models.schemas.customerSchema import customer_schema,customers_schema,customers_value_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache

from utils.util import token_required,role_required

def save():
  try:
    customer_data = customer_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  
  customer_save = customerService.save(customer_data)
  if customer_save is not None:
    return customer_schema.jsonify(customer_save),201
  else:
    return jsonify({"message": "Fallback method error activated", "body":customer_data}), 400

@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200

@token_required
@role_required('admin')
def lifetime_value():
  customers_value = customerService.lifetime_value()
  return customers_value_schema.jsonify(customers_value),200