from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Production(Base):
  __tablename__ = 'Production'
  id: Mapped[int] = mapped_column(primary_key=True)
  product_id: Mapped[int] = mapped_column(db.ForeignKey('Products.id'))
  employee_id: Mapped[int] = mapped_column(db.ForeignKey('Employees.id'))
  quantity: Mapped[int] = mapped_column(db.Integer,nullable=False)
  date: Mapped[datetime.date] = mapped_column(db.Date,nullable=False)
  
  product: Mapped["Product"] = db.relationship(back_populates="production")
  employee: Mapped['Employee'] = db.relationship(back_populates='production')
  