from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select,func
from sqlalchemy.exc import SQLAlchemyError

from models.customer import Customer
from models.product import Product
from models.order import Order
from models.orderProduct import OrderProducts


def fallback_function(customer):
  return None

@circuit(failure_threshold=1,recovery_timeout=10,fallback_function=fallback_function)
def save(customer_data):
  try:
    if customer_data['name'] == "Failure":
      raise Exception("Failure condition triggered")

    with Session(db.engine) as session:
      with session.begin():
        new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
        session.add(new_customer)
        session.commit()  
      session.refresh(new_customer)
      return new_customer     
  except Exception as e:
    raise e

def find_all():
  query = select(Customer)
  customers = db.session.execute(query).scalars().all()
  return customers
      
def lifetime_value():
  query = db.session.query(Customer.name, 
          func.sum(OrderProducts.quantity * Product.price).label('value')).join(Order, 
          Order.customer_id == Customer.id).join(OrderProducts,OrderProducts.order_id == Order.id).join(Product, 
          Product.id == OrderProducts.product_id).group_by(Customer.name).having(func.sum(OrderProducts.quantity * Product.price) > 500).all()
  return query