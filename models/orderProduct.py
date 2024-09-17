from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class OrderProducts(Base):
  __tablename__ = 'Order_product'
  order_id: Mapped[int] = mapped_column(db.ForeignKey('Orders.id'),primary_key = True)
  product_id: Mapped[int] = mapped_column(db.ForeignKey('Products.id'),primary_key = True)
  quantity: Mapped[int] = mapped_column(db.Integer,nullable=False)
  
  order: Mapped['Order'] = db.relationship('Order', back_populates='products')
  product: Mapped['Product'] = db.relationship('Product', back_populates='orders',lazy='joined')