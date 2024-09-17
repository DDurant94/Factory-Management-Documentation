from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List,Dict

class Product(Base):
  __tablename__ = 'Products'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]= mapped_column(db.String(100),nullable=False)
  price: Mapped[float] = mapped_column(db.Float,nullable=False)
  quantity: Mapped[int] = mapped_column(db.Integer,nullable=False)
  
  production: Mapped[List["Production"]] = db.relationship(back_populates="product")
  orders: Mapped[List["OrderProducts"]] = db.relationship('OrderProducts', back_populates='product')