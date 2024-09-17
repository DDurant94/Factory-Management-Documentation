from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv('PASSWORD')

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{PASSWORD}@localhost/factory_management_db'
  CACHE_TYPE = 'SimpleCache'
  DEBUG = True