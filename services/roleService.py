from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select

from models.role import Role
from models.user import User
from models.userManagementRole import UserManagementRole

def save(role_data):
  with Session(db.engine) as session:
    with session.begin():
      new_role = Role(role_name = role_data['role_name'])
      session.add(new_role)
      session.commit()
    session.refresh(new_role)
  return new_role

def find_all():
  query= select(Role)
  roles = db.session.execute(query).scalars().all()
  return roles