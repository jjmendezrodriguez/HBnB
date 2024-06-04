import uuid
from datetime import datetime

class Place:
    def __init__(self, name, description, address, city, latitude, longitude, number_of_rooms, bathrooms, price_per_night, max_guests):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = []
        self.reviews = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.host = None

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)
