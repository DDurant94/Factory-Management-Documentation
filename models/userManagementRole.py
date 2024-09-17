from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class UserManagementRole(Base):
  __tablename__ = "User_Management_Roles"
  id: Mapped[int] = mapped_column(primary_key=True)
  user_management_id: Mapped[int] = mapped_column(db.ForeignKey('Users.id'))
  role_id: Mapped[int] = mapped_column(db.ForeignKey('Roles.id'))