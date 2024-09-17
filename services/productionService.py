from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select,func

from models.production import Production
from models.product import Product

from services.productService import save

def save(production_data):
  with Session(db.engine) as session:
    with session.begin():
      product_id = production_data['product_id']
      product = session.execute(select(Product).where(Product.id==product_id)).scalars().first()
      product.id=product.id 
      product.name=product.name
      product.price=product.price
      product.quantity= product.quantity + production_data["quantity"]
      
      new_production = Production(product_id = production_data["product_id"],employee_id=production_data['employee_id'], quantity = production_data["quantity"], date=production_data["date"])
      session.add(new_production)
      session.commit()
      
    session.refresh(new_production)
    
    return new_production
  
def find_all():
  query = select(Production)
  all_production = db.session.execute(query).scalars().all()
  return all_production

def production_by_date(search_date):
  subquery = db.session.query(Production).filter(Production.date == search_date).subquery()
  query = db.session.query(
    Product.name.label('name'),
    func.sum(subquery.c.quantity).label('total_produced')).join(subquery, Product.id == subquery.c.product_id).group_by(Product.name).all()
  return query