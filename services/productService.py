from sqlalchemy.orm import Session
from database import db
from sqlalchemy import select,func

from models.product import Product
from models.orderProduct import OrderProducts
from models.order import Order


def save(product_data):
  with Session(db.engine) as session:
    with session.begin():
      new_product = Product(name=product_data["name"],price=product_data["price"],quantity=product_data["quantity"])
      session.add(new_product)
      session.commit()
    session.refresh(new_product)
    return new_product
  
def find_all(page=1,per_page=10):
  products = db.paginate(select(Product),page=page,per_page=per_page)
  return products

def find_top_selling_product():
  query = db.session.query(Product.name,
                                  Product.price, 
                                  func.sum(OrderProducts.quantity).label('total_sold')).join(
                                    Order, OrderProducts.order_id == Order.id).join(Product, 
                                                                                    OrderProducts.product_id == Product.id).group_by(Product).order_by(func.sum(OrderProducts.quantity).desc()).all()
  return query