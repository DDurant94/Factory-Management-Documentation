from flask import request, jsonify
from models.schemas.productionSchema import production_schema,all_production_schema,production_on_dates_schema,date_schema
from services import productionService
from marshmallow import ValidationError
from caching import cache

from utils.util import token_required,role_required

@token_required
@role_required('admin')
def save():
  try:
    production_data = production_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    production_save = productionService.save(production_data)
    return production_schema.jsonify(production_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
  all_production = productionService.find_all()
  return all_production_schema.jsonify(all_production),200

@token_required
@role_required('admin')
def production_by_date(date):
  production_on_dates= productionService.production_by_date(date)
  return production_on_dates_schema.jsonify(production_on_dates),200
