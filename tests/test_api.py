import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))

from app import app

class TestCityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)

    def test_get_country(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 200)

    def test_create_city(self):
        response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'US'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_cities(self):
        response = self.app.get('/cities')
        self.assertEqual(response.status_code, 200)

    def test_get_city(self):
        create_response = self.app.post('/cities', json={
            'name': 'Los Angeles',
            'country_code': 'US'
        })
        city_id = create_response.get_json()['id']
        response = self.app.get(f'/cities/{city_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_city(self):
        create_response = self.app.post('/cities', json={
            'name': 'San Francisco',
            'country_code': 'US'
        })
        city_id = create_response.get_json()['id']
        response = self.app.put(f'/cities/{city_id}', json={
            'name': 'San Francisco Updated',
            'country_code': 'US'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_city(self):
        create_response = self.app.post('/cities', json={
            'name': 'San Diego',
            'country_code': 'US'
        })
        city_id = create_response.get_json()['id']
        response = self.app.delete(f'/cities/{city_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
