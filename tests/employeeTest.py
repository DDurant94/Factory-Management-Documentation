import unittest
import os
import sys
import requests
from unittest.mock import MagicMock, patch
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from services.employeeService import save,find_all,employee_production_analyses_query
from models.employee import Employee

def mock_employee_data():
  faker = Faker()
  mock_employee = MagicMock()
  mock_employee.id = 1
  mock_employee.name = faker.name
  mock_employee.position = "Developer"
  return mock_employee

def mock_employees_data():
  faker = Faker()
  mock_employee1 = MagicMock(spec=Employee)
  mock_employee1.id = 1
  mock_employee1.name = faker.name
  mock_employee1.position = "Developer"

  mock_employee2 = MagicMock(spec=Employee)
  mock_employee2.id = 2
  mock_employee2.name = faker.name
  mock_employee2.position = "Manager"
  return [mock_employee1,mock_employee2]

def save_employee_url():
  data = {
    "name": "John Doe",
    "position": "Manager"
  }
  response = requests.post('http://127.0.0.1:5000/employees/add-employee',json=data)
  return response

def find_all_url():
  response = requests.get('http://127.0.0.1:5000/employees/')
  return response

def production_report_url():
  response = requests.get('http://127.0.0.1:5000/employees/production-report')
  return response

class TestEmployeeEndpoints(unittest.TestCase):
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()

# Services Tests    
  @patch('services.employeeService.Session')
  def test_save(self, mock_session):

    mock_session.return_value.__enter__.return_value = mock_session

    employee_data = {
        'name': "Test Employee",
        'position': "Developer"
    }

    response = save(employee_data)

    self.assertIsNotNone(response)
    self.assertEqual(response.name, employee_data['name'])
    self.assertEqual(response.position, employee_data['position'])

  @patch('services.employeeService.db.session.execute')
  def test_find_all(self, mock_execute):
    mock_employees = mock_employees_data()

    mock_execute.return_value.scalars.return_value.all.return_value = mock_employees

    employees = find_all()

    self.assertEqual(len(employees), 2)
    self.assertEqual(employees[0].name, mock_employees[0].name)
    self.assertEqual(employees[1].name, mock_employees[1].name)

  @patch('services.employeeService.db.session.query')
  def test_employee_production_analyses_query(self, mock_query):
    faker = Faker()
    mock_result = MagicMock()
    mock_result.name = faker.name
    mock_result.id = 1
    mock_result.position = "Developer"
    mock_result.total_produced = 100

    mock_query.return_value.join.return_value.join.return_value.group_by.return_value.all.return_value = [mock_result]

    result = employee_production_analyses_query()

    self.assertEqual(len(result), 1)
    self.assertEqual(result[0].name, mock_result.name)
    self.assertEqual(result[0].total_produced, 100)
    
# Endpoint Tests
  @patch('requests.post')
  def test_save_employee_url_success(self, mock_post):
      mock_post.return_value.status_code = 201
      mock_post.return_value.json.return_value = {'message': 'Employee added successfully'}

      response = save_employee_url()

      mock_post.assert_called_once_with('http://127.0.0.1:5000/employees/add-employee',json={"name": "John Doe", "position": "Manager"})
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.json(), {'message': 'Employee added successfully'})

  @patch('requests.post')
  def test_save_employee_url_failure(self, mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {'error': 'Bad Request'}

    response = save_employee_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/employees/add-employee',json={"name": "John Doe", "position": "Manager"})
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})

  @patch('requests.get')
  def test_find_all_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'employee_id': 1, 'name': 'John Doe', 'position': 'Manager'}]

    response = find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/employees/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'employee_id': 1, 'name': 'John Doe', 'position': 'Manager'}])

  @patch('requests.get')
  def test_find_all_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/employees/')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})

  @patch('requests.get')
  def test_production_report_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'report_id': 1, 'details': 'Production report details'}]

    response = production_report_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/employees/production-report')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'report_id': 1, 'details': 'Production report details'}])

  @patch('requests.get')
  def test_production_report_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = production_report_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/employees/production-report')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})
if __name__ == '__main__':
  unittest.main()