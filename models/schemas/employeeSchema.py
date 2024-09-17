from marshmallow import fields,validate
from schema import ma
from sqlalchemy import func

from models.production import Production

class EmployeeSchema(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  position = fields.String(required=True, validate=validate.Length(min=1))
  
  

class EmployeeProduction(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  position = fields.String(required=True, validate=validate.Length(min=1))
  total_produced = fields.Integer(required=False)
  
employee_production_schema = EmployeeProduction()
employees_production_schema = EmployeeProduction(many=True)  

employee_schema = EmployeeSchema()
employees_schema =EmployeeSchema(many=True)