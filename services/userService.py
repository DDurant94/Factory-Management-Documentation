from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select,func
from werkzeug.security import generate_password_hash,check_password_hash

from utils.util import encode_token

from models.user import User
from models.role import Role
from models.userManagementRole import UserManagementRole

def save(user_data):
  with Session(db.engine) as session:
    with session.begin():
      try:
        if 'role' not in user_data.keys():
          savepoint= session.begin_nested()
          new_user = User(username=user_data['username'],password=generate_password_hash(user_data['password']),role='user')
          session.add(new_user)
          session.flush()
        else:
          savepoint= session.begin_nested()
          new_user = User(username=user_data['username'],password=generate_password_hash(user_data['password']),role= user_data['role'])
          session.add(new_user)
          session.flush()
        role = db.session.execute(db.select(Role).where(Role.role_name == new_user.role)).scalar_one_or_none()
        if role is not None:
          adding_user_to_role = UserManagementRole(user_management_id= new_user.id, role_id = role.id)
          session.add(adding_user_to_role)
        else:
          raise ValueError
      except:
        savepoint.rollback()
        return None
      session.commit()
    session.refresh(new_user)
  return new_user
    
def login_user(username,password):
  user = (db.session.execute(db.select(User).where(User.username == username)).unique().scalar_one_or_none())
  if user:
    if check_password_hash(user.password,password):
      
      auth_token = encode_token(user.id,user.role)
      resp = {
        "status": "success",
        "message": "Successfully logged in",
        'auth_token': auth_token
      }
      return resp
    else:
      return None
  else:
    return None
  
def find_all():
  query = select(User)
  users = db.session.execute(query).unique().scalars().all()
  return users