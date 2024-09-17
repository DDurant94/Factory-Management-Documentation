import unittest
import os
import sys
import requests
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from services.orderService import save,find_all
from models.order import Order

def mock_orders_data():
  mock_order1 = MagicMock(spec=Order)
  mock_order1.id = 1
  mock_order1.customer_id = 1
  mock_order1.date = '2024-09-13'

  mock_order2 = MagicMock(spec=Order)
  mock_order2.id = 2
  mock_order2.customer_id = 2
  mock_order2.date = '2024-09-14'
  return [mock_order1,mock_order2]

def save_order_url():
  data = {
    "customer_id": 1,
    "date": "2024-01-01",
    "products":
      [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 2
      }
      ]}
  response = requests.put('http://127.0.0.1:5000/orders/add-order',json=data)
  return response

def find_all_url():
  response = requests.get('http://127.0.0.1:5000/orders/')
  return response

class TestOrderEndpoints(unittest.TestCase):
  def setUp(self):
    self.app = create_app('DevelopmentConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()
    
# Services Tests   
  @patch('services.orderService.Session')
  def test_save(self, mock_session):
    mock_session.return_value.__enter__.return_value = mock_session
    order_data = {
        'customer_id': 1,
        'date': '2024-09-14',
        'products': [{'product_id': 1, 'quantity': 2}, {'product_id': 2, 'quantity': 3}]
    }
    
    mock_product = MagicMock()
    mock_product.id = 1
    mock_product.quantity = 10
    
    mock_customer = MagicMock()
    mock_customer.id = 1
    
    mock_session.execute.return_value.scalars.return_value.all.side_effect = [[mock_product, mock_product],]
    mock_session.execute.return_value.scalars.return_value.first.side_effect = [mock_customer,mock_product,mock_product]
    
    result = save(order_data)
    
    self.assertEqual(len(result.products), 2)
    self.assertEqual(result.customer_id, 1)
    self.assertEqual(result.date, '2024-09-14')
    self.assertEqual(mock_product.quantity, 5)
    
  @patch('services.orderService.Session')
  def test_save_missing_product(self,mock_session):
    mock_session.return_value.__enter__.return_value = mock_session
    
    order_data = {
        'products': [{'product_id': 1, 'quantity': 2}, {'product_id': 3, 'quantity': 3}],
        'customer_id': 1,
        'date': '2024-09-14'
    }
    
    mock_product1 = MagicMock()
    mock_product1.id = 1
    mock_product1.quantity = 10
    mock_customer = MagicMock()
    mock_customer.id = 1
    
    mock_session.execute.return_value.scalars.return_value.all.side_effect = [
        [mock_product1], 
    ]
    mock_session.execute.return_value.scalars.return_value.first.side_effect = [
        mock_customer,
        mock_product1,
        None  
    ]
    
    with self.assertRaises(ValueError) as context:
        save(order_data)
    
    self.assertEqual(str(context.exception), "One or more products do not exist")
          
  @patch('services.orderService.db.paginate')
  def test_find_all(self, mock_paginate):
    mock_orders = mock_orders_data()

    mock_paginate.return_value.items = mock_orders

    orders = find_all(page=1, per_page=10)

    self.assertEqual(len(orders.items), 2)
    self.assertEqual(orders.items[0].id, mock_orders[0].id)
    self.assertEqual(orders.items[1].id, mock_orders[1].id)
    
# Endpoint Tests
  @patch('requests.put')
  def test_save_order_url_success(self, mock_put):
    mock_put.return_value.status_code = 201
    mock_put.return_value.json.return_value = {'message': 'Order added successfully'}

    response = save_order_url()

    mock_put.assert_called_once_with(
        'http://127.0.0.1:5000/orders/add-order',
        json={
            "customer_id": 1,
            "date": "2024-01-01",
            "products": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 2}
            ]
        }
    )
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json(), {'message': 'Order added successfully'})

  @patch('requests.put')
  def test_save_order_url_failure(self, mock_put):
    mock_put.return_value.status_code = 400
    mock_put.return_value.json.return_value = {'error': 'Bad Request'}

    response = save_order_url()

    mock_put.assert_called_once_with(
        'http://127.0.0.1:5000/orders/add-order',
        json={
            "customer_id": 1,
            "date": "2024-01-01",
            "products": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 2}
            ]
        }
    )
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), {'error': 'Bad Request'})

  @patch('requests.get')
  def test_find_all_url_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'order_id': 1, 'customer_id': 1, 'date': '2024-01-01'}]

    response = find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/orders/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), [{'order_id': 1, 'customer_id': 1, 'date': '2024-01-01'}])

  @patch('requests.get')
  def test_find_all_url_failure(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'error': 'Internal Server Error'}

    response = find_all_url()

    mock_get.assert_called_once_with('http://127.0.0.1:5000/orders/')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json(), {'error': 'Internal Server Error'})
      
if __name__ == '__main__':
  unittest.main()