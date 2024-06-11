import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.app import app

class TestCityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 500)

    def test_get_country(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 500)

    def test_create_city(self):
        response = self.app.post('/cities', json={
            'name': 'New York',
            'country_code': 'US'
        })
        self.assertEqual(response.status_code, 500)

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

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_amenity(self):
        response = self.app.post('/amenities', json={'name': 'WiFi'})
        self.assertEqual(response.status_code, 400)

    def test_get_amenities(self):
        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):
        create_response = self.app.post('/amenities', json={'name': 'Pool'})
        amenity_id = create_response.get_json()['id']
        response = self.app.get(f'/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_amenity(self):
        create_response = self.app.post('/amenities', json={'name': 'Gym'})
        amenity_id = create_response.get_json()['id']
        response = self.app.put(f'/amenities/{amenity_id}', json={'name': 'Fitness Center'})
        self.assertEqual(response.status_code, 200)

    def test_delete_amenity(self):
        create_response = self.app.post('/amenities', json={'name': 'Spa'})
        amenity_id = create_response.get_json()['id']
        response = self.app.delete(f'/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 204)

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_review(self):
        create_place_response = self.app.post('/places', json={
            'name': 'Test Place',
            'description': 'A place for testing',
            'address': '123 Test St',
            'city': 'Test City',
            'latitude': 0.0,
            'longitude': 0.0,
            'host_id': 'some-host-id'
        })
        place_id = create_place_response.get_json()['id']

        create_user_response = self.app.post('/users', json={
            'email': 'reviewer@example.com',
            'first_name': 'Reviewer',
            'last_name': 'User'
        })
        user_id = create_user_response.get_json()['id']

        response = self.app.post(f'/places/{place_id}/reviews', json={
            'user_id': user_id,
            'rating': 5,
            'comment': 'Great place!'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_reviews_by_user(self):
        create_user_response = self.app.post('/users', json={
            'email': 'reviewer2@example.com',
            'first_name': 'Reviewer2',
            'last_name': 'User'
        })
        user_id = create_user_response.get_json()['id']
        
        response = self.app.get(f'/users/{user_id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_reviews_by_place(self):
        create_place_response = self.app.post('/places', json={
            'name': 'Test Place 2',
            'description': 'Another place for testing',
            'address': '456 Test St',
            'city': 'Test City',
            'latitude': 0.0,
            'longitude': 0.0,
            'host_id': 'another-host-id'
        })
        place_id = create_place_response.get_json()['id']
        
        response = self.app.get(f'/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_review(self):
        create_review_response = self.app.post(f'/places/some-place-id/reviews', json={
            'user_id': 'some-user-id',
            'rating': 5,
            'comment': 'Great place!'
        })
        review_id = create_review_response.get_json()['id']
        
        response = self.app.get(f'/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_review(self):
        create_review_response = self.app.post(f'/places/some-place-id/reviews', json={
            'user_id': 'some-user-id',
            'rating': 5,
            'comment': 'Great place!'
        })
        review_id = create_review_response.get_json()['id']
        
        response = self.app.put(f'/reviews/{review_id}', json={
            'rating': 4,
            'comment': 'Updated comment'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        create_review_response = self.app.post(f'/places/some-place-id/reviews', json={
            'user_id': 'some-user-id',
            'rating': 5,
            'comment': 'Great place!'
        })
        review_id = create_review_response.get_json()['id']
        
        response = self.app.delete(f'/reviews/{review_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
