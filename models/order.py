from typing import List
from database import db, Base
import datetime
from sqlalchemy.orm import Mapped, mapped_column

class Order(Base):
  __tablename__ = 'Orders'
  id: Mapped[int] = mapped_column(primary_key=True)
  customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'))
  date: Mapped[datetime.date] = mapped_column(db.Date,nullable=False)
  
  customer: Mapped["Customer"] = db.relationship(back_populates="orders")
  products: Mapped[List["OrderProducts"]] = db.relationship('OrderProducts', back_populates='order')