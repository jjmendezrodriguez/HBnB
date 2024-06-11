from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models import Amenity, Country, City, Place, Review, User
from datetime import datetime
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Initialize DataManager for persistence
data_manager = DataManager()

# Pre-loaded country data
preloaded_countries = [
    Country(name="United States", code="US"),
    Country(name="Canada", code="CA"),
    Country(name="Mexico", code="MX"),
    # Add more countries as needed
]

# Save pre-loaded countries to data manager
for country in preloaded_countries:
    data_manager.save(country)

# Utility functions
def is_valid_country_code(code):
    """
    Check if a country code is valid.
    """
    return any(country.code == code for country in preloaded_countries)

def is_non_empty_string(s):
    """
    Check if a string is non-empty and not just whitespace.
    """
    return isinstance(s, str) and bool(s.strip())

def is_valid_email(email):
    """
    Check if an email is valid using regex.
    """
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None

def is_valid_rating(rating):
    """
    Check if a rating is an integer between 1 and 5.
    """
    return isinstance(rating, int) and 1 <= rating <= 5

# Custom JSON encoder for complex objects
class CustomJSONEncoder():
    def default(self, obj):
        """
        Custom JSON serialization for complex objects.
        """
        if isinstance(obj, Country):
            return {"name": obj.name, "code": obj.code}
        if isinstance(obj, City):
            return {"id": obj.id, "name": obj.name, "country": self.default(obj.country)}
        if isinstance(obj, Amenity):
            return {"id": obj.id, "name": obj.name, "description": obj.description}
        if isinstance(obj, User):
            return {"id": obj.id, "email": obj.email, "first_name": obj.first_name, "last_name": obj.last_name}
        if isinstance(obj, Review):
            return {"id": obj.id, "place": self.default(obj.place), "user": self.default(obj.user), "rating": obj.rating, "comment": obj.comment}
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# Country and City Endpoints
@app.route('/countries', methods=['GET'])
def get_countries():
    """
    Retrieve all pre-loaded countries.
    """
    countries = data_manager.storage.get('Country', [])
    return jsonify(countries), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    """
    Retrieve details of a specific country by its code.
    """
    country = data_manager.get(country_code, 'Country')
    if country:
        return jsonify(country), 200
    else:
        return jsonify({"error": "Country not found"}), 404

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    """
    Retrieve all cities belonging to a specific country.
    """
    country = data_manager.get(country_code, 'Country')
    if country:
        cities = [city for city in data_manager.storage.get('City', []) if city['country_code'] == country_code]
        return jsonify(cities), 200
    else:
        return jsonify({"error": "Country not found"}), 404

# City endpoints
@app.route('/cities', methods=['POST'])
def create_city():
    """
    Create a new city.
    """
    data = request.json
    city = City(id=data['id'], name=data['name'], country_code=data['country_code'])
    data_manager.save(city)
    return jsonify(city), 201

@app.route('/cities', methods=['GET'])
def get_cities():
    """
    Retrieve all cities.
    """
    cities = data_manager.storage.get('City', [])
    return jsonify(cities), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Retrieve details of a specific city.
    """
    city = data_manager.get(city_id, 'City')
    if city:
        return jsonify(city), 200
    else:
        return jsonify({"error": "City not found"}), 404

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Update an existing city's information.
    """
    data = request.json
    city = data_manager.get(city_id, 'City')
    if city:
        for key, value in data.items():
            setattr(city, key, value)
        data_manager.update(city)
        return jsonify(city), 200
    else:
        return jsonify({"error": "City not found"}), 404

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Delete a specific city.
    """
    try:
        data_manager.delete(city_id, 'City')
        return '', 204
    except ValueError:
        return jsonify({"error": "City not found"}), 404

# Amenity endpoints
@app.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Create a new amenity.
    """
    data = request.json
    amenity = Amenity(id=data['id'], name=data['name'])
    data_manager.save(amenity)
    return jsonify(amenity), 201

@app.route('/amenities', methods=['GET'])
def get_amenities():
    """
    Retrieve a list of all amenities.
    """
    amenities = data_manager.storage.get('Amenity', [])
    return jsonify(amenities), 200

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieve detailed information about a specific amenity.
    """
    amenity = data_manager.get(amenity_id, 'Amenity')
    if amenity:
        return jsonify(amenity), 200
    else:
        return jsonify({"error": "Amenity not found"}), 404

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Update an existing amenity's information.
    """
    data = request.json
    amenity = data_manager.get(amenity_id, 'Amenity')
    if amenity:
        for key, value in data.items():
            setattr(amenity, key, value)
        data_manager.update(amenity)
        return jsonify(amenity), 200
    else:
        return jsonify({"error": "Amenity not found"}), 404

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete a specific amenity.
    """
    try:
        data_manager.delete(amenity_id, 'Amenity')
        return '', 204
    except ValueError:
        return jsonify({"error": "Amenity not found"}), 404

# Place endpoints
@app.route('/places', methods=['POST'])
def create_place():
    """
    Create a new place.
    """
    data = request.json
    place = Place(id=data['id'], name=data['name'], description=data['description'], city_id=data['city_id'],
                  host_id=data['host_id'], latitude=data['latitude'], longitude=data['longitude'], 
                  price_per_night=data['price_per_night'], max_guests=data['max_guests'], 
                  number_of_rooms=data['number_of_rooms'], number_of_bathrooms=data['number_of_bathrooms'], 
                  amenity_ids=data['amenity_ids'])
    data_manager.save(place)
    return jsonify(place), 201

@app.route('/places', methods=['GET'])
def get_places():
    """
    Retrieve a list of all places.
    """
    places = data_manager.storage.get('Place', [])
    return jsonify(places), 200

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieve detailed information about a specific place.
    """
    place = data_manager.get(place_id, 'Place')
    if place:
        return jsonify(place), 200
    else:
        return jsonify({"error": "Place not found"}), 404

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Update an existing place's information.
    """
    data = request.json
    place = data_manager.get(place_id, 'Place')
    if place:
        for key, value in data.items():
            setattr(place, key, value)
        data_manager.update(place)
        return jsonify(place), 200
    else:
        return jsonify({"error": "Place not found"}), 404

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Delete a specific place.
    """
    try:
        data_manager.delete(place_id, 'Place')
        return '', 204
    except ValueError:
        return jsonify({"error": "Place not found"}), 404

# User endpoints
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    """
    data = request.json
    user = User(id=data['id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
    data_manager.save(user)
    return jsonify(user), 201

@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve a list of all users.
    """
    users = data_manager.storage.get('User', [])
    return jsonify(users), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve detailed information about a specific user.
    """
    user = data_manager.get(user_id, 'User')
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user's information.
    """
    data = request.json
    user = data_manager.get(user_id, 'User')
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        data_manager.update(user)
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a specific user.
    """
    try:
        data_manager.delete(user_id, 'User')
        return '', 204
    except ValueError:
        return jsonify({"error": "User not found"}), 404

# Review endpoints
@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Create a new review for a specified place.
    """
    data = request.json
    review = Review(id=data['id'], user_id=data['user_id'], place_id=place_id, rating=data['rating'], comment=data['comment'])
    data_manager.save(review)
    return jsonify(review), 201

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    """
    Retrieve all reviews written by a specific user.
    """
    reviews = [review for review in data_manager.storage.get('Review', {}).values() if review.user_id == user_id]
    return jsonify(reviews), 200

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """
    Retrieve all reviews for a specific place.
    """
    reviews = [review for review in data_manager.storage.get('Review', {}).values() if review.place_id == place_id]
    return jsonify(reviews), 200

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieve detailed information about a specific review.
    """
    review = data_manager.get(review_id, 'Review')
    if review:
        return jsonify(review), 200
    else:
        return jsonify({"error": "Review not found"}), 404

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update an existing review.
    """
    data = request.json
    review = data_manager.get(review_id, 'Review')
    if review:
        for key, value in data.items():
            setattr(review, key, value)
        data_manager.update(review)
        return jsonify(review), 200
    else:
        return jsonify({"error": "Review not found"}), 404

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a specific review.
    """
    try:
        data_manager.delete(review_id, 'Review')
        return '', 204
    except ValueError:
        return jsonify({"error": "Review not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
