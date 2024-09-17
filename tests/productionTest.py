import unittest
import os
import sys
import requests
from unittest.mock import MagicMock, patch
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.productionService import save,find_all,production_by_date
from app import create_app
from models.production import Production

def mock_product_data():
  faker = Faker()
  mock_product = MagicMock()
  mock_product.id = 1
  mock_product.name = "Test Product"
  mock_product.price = faker.pricetag
  mock_product.quantity = 100
  return mock_product

def mock_production_data():
  mock_production1 = MagicMock(spec=Production)
  mock_production1.id = 1
  mock_production1.product_id = 1
  mock_production1.employee_id = 1
  mock_production1.quantity = 50
  mock_production1.date = '2024-09-13'

  mock_production2 = MagicMock(spec=Production)
  mock_production2.id = 2
  mock_production2.product_id = 2
  mock_production2.employee_id = 2
  mock_production2.quantity = 100
  mock_production2.date = '2024-09-14'
  return [mock_production1,mock_production2]

def production_save_url():
  data = {
    "product_id": 1,
    "quantity": 100,
    "date": "2024-01-01"
}
  response = requests.post('http://127.0.0.1:5000/production/add-production-product',json=data)
  return response

def production_find_all_url():
  response = requests.get('http://127.0.0.1:5000/production/')
  return response

def production_by_date_url():
  response= requests.get('http://127.0.0.1:5000/production/production-by-date/2024-01-03')
  return response
class TestProductionEndpoints(unittest.TestCase):
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()

# Services Tests    
  @patch('services.productionService.db.session.execute')
  @patch('services.productionService.Session')
  def test_save(self, mock_session, mock_execute):
    mock_product = mock_product_data()

    mock_session.return_value.__enter__.return_value = mock_session
    mock_execute.return_value.scalars.return_value.first.return_value = mock_product

    production_data = {
        'product_id': 1,
        'employee_id': 1,
        'quantity': 50,
        'date': '2024-09-13'
    }

    response = save(production_data)

    self.assertIsNotNone(response)
    self.assertEqual(response.product_id, production_data['product_id'])
    self.assertEqual(response.quantity, production_data['quantity'])
    self.assertEqual(response.date, production_data['date'])

  @patch('services.productionService.db.session.execute')
  def test_find_all(self, mock_execute):
    mock_production = mock_production_data()

    mock_execute.return_value.scalars.return_value.all.return_value = mock_production

    all_production = find_all()

    self.assertEqual(len(all_production), 2)
    self.assertEqual(all_production[0].quantity, mock_production[0].quantity)
    self.assertEqual(all_production[1].quantity, mock_production[1].quantity)

  @patch('services.productionService.db.session.query')
  def test_production_by_date(self, mock_query):
    mock_result = MagicMock()
    mock_result.name = "Test Product"
    mock_result.total_produced = 50

    mock_query.return_value.join.return_value.group_by.return_value.all.return_value = [mock_result]

    search_date = '2024-09-13'
    result = production_by_date(search_date)

    self.assertEqual(len(result), 1)
    self.assertEqual(result[0].name, "Test Product")
    self.assertEqual(result[0].total_produced, 50)
    
# Endpoints Tests
  @patch('requests.post')
  def test_production_save_url_success(self, mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {'message': 'Production added successfully'}

    response = production_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/production/add-production-product',json={"product_id": 1, "quantity": 100, "date": "2024-01-01"})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json(), {'message': 'Production added successfully'})

  @patch('requests.post')
  def test_production_save_url_failure(self, mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {'error': 'Bad Request'}

    response = production_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/production/add-production-product',json={"product_id": 1, "quantity": 100, "date": "2024-01-01"})
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})

  @patch('requests.get')
  def test_production_find_all_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}]

    response = production_find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/production/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}])

  @patch('requests.get')
  def test_production_find_all_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = production_find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/production/')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})

  @patch('requests.get')
  def test_production_by_date_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}]

    response = production_by_date_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/production/production-by-date/2024-01-03')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}])

  @patch('requests.get')
  def test_production_by_date_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = production_by_date_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/production/production-by-date/2024-01-03')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})

if __name__ == '__main__':
  unittest.main()