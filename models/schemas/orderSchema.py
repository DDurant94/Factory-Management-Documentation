from marshmallow import fields
from schema import ma

class OrderSchema(ma.Schema):
  id = fields.Integer(required=False)
  date = fields.Date(required=True)
  customer_id = fields.Integer(required=True)
  products = fields.List(fields.Nested(lambda:OrderProductSchema), required=True)
  
  
class OrderProductSchema(ma.Schema):
  product_id = fields.Integer(required=True)
  quantity = fields.Integer(required=True)
  product = fields.Nested('ProductSchema')
  
  
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

