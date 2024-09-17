from unittest.mock import MagicMock, patch
import unittest
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.roleService import save,find_all
from models.role import Role
from app import create_app

def mock_role_data():
  mock_role = MagicMock(spec=Role)
  mock_role.id = 1
  mock_role.role_name = 'user'
  return mock_role

def mock_roles_data():
  mock_role1 = MagicMock(spec=Role)
  mock_role1.id = 1
  mock_role1.role_name = "admin"

  mock_role2 = MagicMock(spec=Role)
  mock_role2.id = 2
  mock_role2.role_name = "user"
  
  return [mock_role1,mock_role2]

def role_save_url():
  data = {
    "role_name": "admin"
  }
  response = requests.post('http://127.0.0.1:5000/roles/add-role',json=data)
  return response

def role_find_all_url():
  find_all_role_url = requests.get('http://127.0.0.1:5000/roles/')
  return find_all_role_url

class TestRoleEndpoints(unittest.TestCase):
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()

# Services Tests 
  @patch('services.roleService.db.session.execute')
  @patch('services.roleService.Session')
  def test_save(self, mock_session, mock_execute):
    mock_role = mock_role_data()

    mock_session.return_value.__enter__.return_value = mock_session
    mock_execute.return_value.scalar_one_or_none.return_value = mock_role

    role_data = {
        'role_name': "admin"
    }

    response = save(role_data)

    self.assertIsNotNone(response)
    self.assertEqual(response.role_name, role_data['role_name'])

  @patch('services.roleService.Session')
  def test_save_exception(self, mock_session):
    mock_session_instance = mock_session.return_value.__enter__.return_value
    mock_session_instance.commit.side_effect = Exception("Commit failed")

    role_data = {'role_name': 'Admin'}
    with self.assertRaises(Exception) as context:
        save(role_data)

    self.assertTrue('Commit failed' in str(context.exception))
    mock_session_instance.add.assert_called_once()
    mock_session_instance.commit.assert_called_once()

  @patch('services.roleService.db.session.execute')
  def test_find_all(self, mock_execute):
    mock_roles = mock_roles_data()

    mock_execute.return_value.scalars.return_value.all.return_value = mock_roles

    roles = find_all()

    self.assertEqual(len(roles), 2)
    self.assertEqual(roles[0].role_name, mock_roles[0].role_name)
    self.assertEqual(roles[1].role_name, mock_roles[1].role_name)
    
  @patch('services.roleService.db.session.execute')
  def test_find_all_exception(self, mock_execute):
    mock_execute.side_effect = Exception("Query failed")

    with self.assertRaises(Exception) as context:
        find_all()

    self.assertTrue('Query failed' in str(context.exception))
    mock_execute.assert_called_once()
  
  
# Endpoint Tests
  @patch('requests.post')
  def test_role_save_url_success(self, mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {'message': 'Role added successfully'}

    response = role_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/roles/add-role',json={"role_name": "admin"})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json(), {'message': 'Role added successfully'})

  @patch('requests.post')
  def test_role_save_url_failure(self, mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {'error': 'Bad Request'}

    response = role_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/roles/add-role',json={"role_name": "admin"})
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})

  @patch('requests.get')
  def test_role_find_all_url(self, mock_get):
      mock_get.return_value.status_code = 200
      mock_get.return_value.json.return_value = [{'id': 1, 'name': 'Admin'}]

      response = role_find_all_url()

      mock_get.assert_called_once_with('http://127.0.0.1:5000/roles/')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json(), [{'id': 1, 'name': 'Admin'}])
      
  @patch('requests.get')
  def test_role_find_all_url_failure(self, mock_get):
      mock_get.return_value.status_code = 400
      mock_get.return_value.json.return_value = {'error': 'Connection Error'}

      response = role_find_all_url()

      mock_get.assert_called_once_with('http://127.0.0.1:5000/roles/')
      self.assertEqual(response.status_code, 400)
      self.assertEqual(response.json(), {'error': 'Connection Error'})
  
if __name__ == '__main__':
  unittest.main()