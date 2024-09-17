import unittest
import os
import sys
import requests
from unittest.mock import MagicMock, patch
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.productService import save,find_all,find_top_selling_product
from models.schemas.productSchema import product_schema,products_schema
from app import create_app
from models.product import Product

def mock_product_data():
  faker = Faker()
  mock_product = MagicMock()
  mock_product.id = 1
  mock_product.name = faker.random_object_name
  mock_product.price = 10.0
  mock_product.quantity = 100
  return mock_product

def mock_products_data():
  faker = Faker()
  mock_product1 = MagicMock(spec=Product)
  mock_product1.id = 1
  mock_product1.name = 'product1'
  mock_product1.price = faker.pricetag
  mock_product1.quantity = 100

  mock_product2 = MagicMock(spec=Product)
  mock_product2.id = 2
  mock_product2.name = 'product2'
  mock_product2.price = faker.pricetag
  mock_product2.quantity = 200
  
  return [mock_product1,mock_product2]

def product_save_url():
  data ={

    "product_id": 1,
    "quantity": 100,
    "date": "2024-01-01"
  }
  save_url = requests.post('http://127.0.0.1:5000/products/add-product',json=data)
  return save_url

def product_find_all_url():
  find_all_url = requests.get('http://127.0.0.1:5000/products/')
  return find_all_url

def product_top_selling_url():
  top_selling_url = requests.get('http://127.0.0.1:5000/products/top-selling')
  return top_selling_url  

class TestProductEndpoints(unittest.TestCase):
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()
    
# Testing Services 
  @patch('services.productService.Session')
  def test_save(self, mock_session):

    mock_session.return_value.__enter__.return_value = mock_session

    product_data = {
        'name': "Test Product",
        'price': 10.0,
        'quantity': 100
    }

    response = save(product_data)

    self.assertIsNotNone(response)
    self.assertEqual(response.name, product_data['name'])
    self.assertEqual(response.price, product_data['price'])
    self.assertEqual(response.quantity, product_data['quantity'])

  @patch('services.productService.Session')
  def test_save_exception(self, mock_session):

      mock_session_instance = mock_session.return_value.__enter__.return_value
      mock_session_instance.commit.side_effect = Exception("Commit failed")

      product_data = {'name': 'Laptop', 'price': 1000, 'quantity': 10}
      with self.assertRaises(Exception) as context:
        save(product_data)
          
      self.assertTrue('Commit failed' in str(context.exception))
      mock_session_instance.add.assert_called_once()
      mock_session_instance.commit.assert_called_once()

  @patch('services.productService.db.paginate')
  def test_find_all(self, mock_paginate):
    mock_products = mock_products_data()

    mock_paginate.return_value.items = mock_products

    products = find_all(page=1, per_page=10)

    self.assertEqual(len(products.items), 2)
    self.assertEqual(products.items[0].name, mock_products[0].name)
    self.assertEqual(products.items[1].name, mock_products[1].name)

  @patch('services.productService.db.paginate')
  def test_find_all_exception(self, mock_paginate):

      mock_paginate.side_effect = Exception("Query failed")

      with self.assertRaises(Exception) as context:
          find_all(page=1, per_page=10)

      self.assertTrue('Query failed' in str(context.exception))
      mock_paginate.assert_called_once()

  @patch('services.productService.db.session.query')
  def test_find_top_selling_product(self, mock_query):
    mock_product = MagicMock()
    mock_product.name = "Top Product"
    mock_product.price = 15.0
    mock_product.total_sold = 50

    mock_query.return_value.join.return_value.join.return_value.group_by.return_value.order_by.return_value.all.return_value = [mock_product]

    top_selling_product = find_top_selling_product()

    self.assertEqual(len(top_selling_product), 1)
    self.assertEqual(top_selling_product[0].name, "Top Product")
    self.assertEqual(top_selling_product[0].total_sold, 50)
    
  @patch('services.productService.db.session.query')
  def test_find_top_selling_product_exception(self, mock_query):
    
    mock_query.side_effect = Exception("Query failed")

    with self.assertRaises(Exception) as context:
        find_top_selling_product()

    self.assertTrue('Query failed' in str(context.exception))
    mock_query.assert_called_once()

# Testing Endpoints
  @patch('requests.post')
  def test_product_save_url_success(self, mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {'message': 'Product added successfully'}

    response = product_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/products/add-product',json={"product_id": 1, "quantity": 100, "date": "2024-01-01"})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json(), {'message': 'Product added successfully'})

  @patch('requests.post')
  def test_product_save_url_failure(self, mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {'error': 'Bad Request'}

    response = product_save_url()

    mock_post.assert_called_once_with('http://127.0.0.1:5000/products/add-product',json={"product_id": 1, "quantity": 100, "date": "2024-01-01"})
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})

  @patch('requests.get')
  def test_product_find_all_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}]
    
    response = product_find_all_url()
    
    mock_get.assert_called_once_with('http://127.0.0.1:5000/products/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}])

  @patch('requests.get')
  def test_product_find_all_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}
    
    response = product_find_all_url()
    
    mock_get.assert_called_once_with('http://127.0.0.1:5000/products/')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})

  @patch('requests.get')
  def test_product_top_selling_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}]
    response = product_top_selling_url()
    mock_get.assert_called_once_with('http://127.0.0.1:5000/products/top-selling')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'product_id': 1, 'quantity': 100, 'date': '2024-01-01'}])

  @patch('requests.get')
  def test_product_top_selling_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}
    
    response = product_top_selling_url()
    
    mock_get.assert_called_once_with('http://127.0.0.1:5000/products/top-selling')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})

if __name__ == '__main__':
  unittest.main()