from marshmallow import fields
from schema import ma

class ProductionSchema(ma.Schema):
  id = fields.Integer(required=False)
  product_id= fields.Integer(required=True)
  employee_id = fields.Integer(required=True)
  quantity = fields.Integer(required=True)
  date = fields.Date(required=True)
  
  
class ProductionOnDatesSchema(ma.Schema):
  name = fields.String(required=True)
  total_produced = fields.Integer(required=True)
  
  
class DateSchema(ma.Schema):
  date = fields.Date(required=True)
    
production_on_dates_schema = ProductionOnDatesSchema(many=True)
date_schema = DateSchema()

production_schema = ProductionSchema()
all_production_schema = ProductionSchema(many=True)
  
  