import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.location import Country, City

class TestModels(unittest.TestCase):
    def test_user_creation(self):
        user = User(email="test@example.com", password="password", first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_place_creation(self):
        city = City(name="New York", country_code="US")
        place = Place(name="Test Place", description="A place for testing", city_id=city.id, host_id="host-id",
                  latitude=0.0, longitude=0.0, price_per_night=100.0, max_guests=4, number_of_rooms=2, number_of_bathrooms=1,
                  amenity_ids=[])
        self.assertEqual(place.name, "Test Place")
        self.assertEqual(place.city_id, city.id)


    def test_review_creation(self):
        user = User(email="test@example.com", password="password", first_name="John", last_name="Doe")
        place = Place(name="Test Place", description="A place for testing", city_id="city-id", host_id="host-id",
                  latitude=0.0, longitude=0.0, price_per_night=100.0, max_guests=4, number_of_rooms=2, number_of_bathrooms=1,
                  amenity_ids=[])
        review = Review(user_id=user.id, place_id=place.id, rating=5, comment="Great place!")
        self.assertEqual(review.user_id, user.id)
        self.assertEqual(review.place_id, place.id)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great place!")

    def test_amenity_creation(self):
        amenity = Amenity(name="WiFi", description="Free WiFi")
        self.assertIsNotNone(amenity.id)
        self.assertEqual(amenity.name, "WiFi")

if __name__ == "__main__":
    unittest.main()
