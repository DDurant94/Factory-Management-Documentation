from sqlalchemy.orm import Session
from sqlalchemy import select,Subquery
from database import db

from models.order import Order
from models.customer import Customer
from models.product import Product
from models.orderProduct import OrderProducts

def save(order_data):
  with Session(db.engine) as session:
    with session.begin():
      product_ids = [product['product_id'] for product in order_data['products']]
      products = session.execute(select(Product).where(Product.id.in_(product_ids))).scalars().all()
      
      customer_id = order_data['customer_id']
      customer = session.execute(select(Customer).where(Customer.id == customer_id)).scalars().first()
      
      if len(products) != len(product_ids):
        raise ValueError("One or more products do not exist")
      
      if not customer:
        raise ValueError(f"Customer with ID {customer_id} does not exist")
      
      new_order = Order(date=order_data['date'], customer_id=customer_id,products=[])
      session.add(new_order)
      session.flush()
      
      for product_data in order_data['products']:
        
        product_id = product_data['product_id']
        quantity = product_data['quantity']
        
        order_products = OrderProducts(order_id=new_order.id, product_id=product_id,quantity= quantity)
        
        product = session.execute(select(Product).where(Product.id == product_id)).scalars().first()
        
        product.quantity -= quantity
        
        session.add(order_products)
        
        new_order.products.append(order_products) 
        
      session.commit()
      session.flush()
    session.refresh(new_order)
    
    for product in new_order.products:
      session.refresh(product)
      
    return new_order
  
def find_all(page=1,per_page=10):
  subquery = select(OrderProducts.order_id).join(Product,OrderProducts.product_id == Product.id).subquery()
  orders=db.paginate(select(Order).join(OrderProducts, Order.id == OrderProducts.order_id).join(
    Product, OrderProducts.product_id == Product.id).where(
    Order.id.in_(select(subquery.c.order_id))).group_by(Order.id),page=page,per_page=per_page)
  return orders