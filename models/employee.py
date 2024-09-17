from database import db,Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Employee(Base):
  __tablename__ = 'Employees'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(db.String(100),nullable=False)
  position: Mapped[str] = mapped_column(db.String(100),nullable=False)
  
  production: Mapped[List["Production"]] = db.relationship(back_populates="employee")