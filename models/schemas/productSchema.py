from marshmallow import fields, validate
from schema import ma

class ProductSchema(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  price = fields.Float(required=True, validate=validate.Range(min=0))
  quantity = fields.Integer(required=True, validate=validate.Range(min=0))
  
class TopSellingProductSchema(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  price = fields.Float(required=True, validate=validate.Range(min=0))
  total_sold = fields.Integer(required=True, validate=validate.Range(min=0))
  
top_selling_product_schema = TopSellingProductSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)