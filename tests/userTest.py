import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from werkzeug.security import generate_password_hash,check_password_hash
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.userService import login_user,save,find_all
from models.role import Role
from models.user import User
from app import create_app

def mock_user_data():
  faker = Faker()
  mock_user = MagicMock(spec=User)
  mock_user.id = 1
  mock_user.username = faker.user_name()
  mock_user.password = generate_password_hash(faker.password())
  mock_user.role = 'user'
  mock_user.roles = [MagicMock(role_name='user'),MagicMock(role_name='admin')]
  return mock_user

def mock_role_data():
    mock_role = MagicMock(spec=Role)
    mock_role.id = 1
    mock_role.role_name = 'user'
    return mock_role

def user_save_url():
    data = {
        "username": "UsEr1",
        "password": "PassWord1",
        "role": "admin"
    }

    response = requests.post('http://127.0.0.1:5000/users/add-user', json=data)
    return response

def user_find_all_url():
  response = requests.get('http://127.0.0.1:5000/users/')
  return response

def user_login_url():
  data = {
      "username": "DDurant94",
      "password": "password1"
  }
  response = requests.post('http://127.0.0.1:5000/users/login', json=data)
  return response

class TestLoginUser(unittest.TestCase):
  
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()

# Services Tests
  @patch('services.userService.db.session.execute')
  @patch('services.userService.Session')
  def test_save_user(self, mock_session, mock_execute):
    faker = Faker()
    mock_user = mock_user_data()
    mock_role = mock_role_data()
    mock_execute.return_value.scalar_one_or_none.return_value = mock_role
    mock_session.return_value.__enter__.return_value = mock_session

    user_data = {
        'username': mock_user.username,
        'password': faker.password()
    }

    response = save(user_data)
    mock_session.return_value.__exit__.return_value = mock_session

    self.assertIsNotNone(response)
    self.assertEqual(response.username, mock_user.username)
    self.assertEqual(response.role, 'user')

  @patch('services.userService.db.session.execute')
  @patch('services.userService.Session')
  def test_save_user_with_role(self, mock_session, mock_execute):
    faker = Faker()
    mock_user = mock_user_data()
    mock_role = mock_role_data()

    mock_execute.return_value.scalar_one_or_none.return_value = mock_role
    mock_session.return_value.__enter__.return_value = mock_session

    user_data = {
        'username': mock_user.username,
        'password': faker.password(),
        'role': 'admin'
    }

    response = save(user_data)

    self.assertIsNotNone(response)
    self.assertEqual(response.username, mock_user.username)
    self.assertEqual(response.role, 'admin')
  
  @patch('services.userService.db.session.execute')
  def test_login_user(self,mock_customer):
    faker = Faker()
    mock_user = MagicMock()
    mock_user.id = 1
    password = faker.password()
    mock_user.username = faker.user_name()
    mock_user.password = generate_password_hash(password)
    mock_user.role = 'admin'
    mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
    
    mock_customer.return_value.unique.return_value.scalar_one_or_none.return_value = mock_user
    
    response = login_user(mock_user.username,password)
    
    self.assertEqual(response['status'],'success')
      
  @patch('services.userService.db.session.execute')
  def test_login_user_wrong_password(self,mock_customer):
    faker = Faker()
    mock_user = MagicMock()
    mock_user.id =1
    mock_user.role = "admin"
    mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
    password = faker.password()
    mock_user.username = faker.user_name()
    mock_user.password = generate_password_hash(password)
    mock_customer.return_value.unique.return_value.scalar_one_or_none.return_value = mock_user
    
    response = login_user(mock_user.username,faker.password())
    
    self.assertIsNone(response)
    
  @patch('services.userService.db.session.execute')
  def test_login_user_nonexistent_user(self, mock_execute):
    mock_execute.return_value.unique.return_value.scalar_one_or_none.return_value = None

    response = login_user('nonexistent', 'password123')

    self.assertIsNone(response)
  
  @patch('services.userService.db.session.execute')
  def test_find_all(self,mock_customer):
    faker = Faker()
    mock_user = mock_user_data()
    password = faker.password()
    mock_user.username = faker.user_name()
    mock_user.password = generate_password_hash(password)
    mock_customer.return_value.unique.return_value.scalars.all.return_value = mock_user
    
    response = find_all()
    
    self.assertTrue(response)
  
# Endpoints Tests
  @patch('requests.post')
  def test_user_save_url_success(self, mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {'message': 'User added successfully'}
    
    response = user_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/users/add-user',json={"username": "UsEr1", "password": "PassWord1", "role": "admin"})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json(), {'message': 'User added successfully'})

  @patch('requests.post')
  def test_user_save_url_failure(self, mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {'error': 'Bad Request'}

    response = user_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/users/add-user',json={"username": "UsEr1", "password": "PassWord1", "role": "admin"})
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})

  @patch('requests.get')
  def test_user_find_all_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'user_id': 1, 'username': 'UsEr1', 'role': 'admin'}]

    response = user_find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/users/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'user_id': 1, 'username': 'UsEr1', 'role': 'admin'}])

  @patch('requests.get')
  def test_user_find_all_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = user_find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/users/')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})

  @patch('requests.post')
  def test_user_login_url_success(self, mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'message': 'Login successful'}

    response = user_login_url()

    mock_post.assert_called_once_with(
        'http://127.0.0.1:5000/users/login',
        json={"username": "DDurant94", "password": "password1"}
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Login successful'})

  @patch('requests.post')
  def test_user_login_url_failure(self, mock_post):
    mock_post.return_value.status_code = 401
    mock_post.return_value.json.return_value = {'error': 'Unauthorized'}

    response = user_login_url()

    mock_post.assert_called_once_with(
        'http://127.0.0.1:5000/users/login',
        json={"username": "DDurant94", "password": "password1"}
    )
    self.assertEqual(response.status_code, 401)
    self.assertEqual(response.json(), {'error': 'Unauthorized'})
      
if __name__ == '__main__':
  unittest.main()
