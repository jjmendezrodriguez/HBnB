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
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")

    def test_place_creation(self):
        city = City(name="New York", country=Country(name="USA", code="US"))
        place = Place(name="Test Place", description="A place to test", address="123 Test St", city=city, latitude=40.7128, longitude=-74.0060, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        self.assertIsNotNone(place.id)
        self.assertEqual(place.city.name, "New York")

    def test_review_creation(self):
        user = User(email="test@example.com", password="password", first_name="John", last_name="Doe")
        place = Place(name="Test Place", description="A place to test", address="123 Test St", city=City(name="New York", country=Country(name="USA", code="US")), latitude=40.7128, longitude=-74.0060, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=4)
        review = Review(rating=5, comment="Great place!", place=place, user=user)
        self.assertIsNotNone(review.id)
        self.assertEqual(review.rating, 5)

    def test_amenity_creation(self):
        amenity = Amenity(name="WiFi", description="Free WiFi")
        self.assertIsNotNone(amenity.id)
        self.assertEqual(amenity.name, "WiFi")

if __name__ == "__main__":
    unittest.main()
