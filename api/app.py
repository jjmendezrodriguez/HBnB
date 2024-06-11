from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.location import Country, City
from models.amenity import Amenity
from models.user import User
from models.review import Review
from datetime import datetime
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
data_manager = DataManager()

# Pre-loaded country data
preloaded_countries = [
    Country(name="United States", code="US"),
    Country(name="Canada", code="CA"),
    Country(name="Mexico", code="MX"),
    # Add more countries as needed
]

for country in preloaded_countries:
    data_manager.save(country)

# Utility functions
def is_valid_country_code(code):
    return any(country.code == code for country in preloaded_countries)

def is_non_empty_string(s):
    return isinstance(s, str) and bool(s.strip())

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None

def is_valid_rating(rating):
    return isinstance(rating, int) and 1 <= rating <= 5

# Custom JSON encoder for complex objects
class CustomJSONEncoder():
    def default(self, obj):
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
    countries = [country for country in preloaded_countries]
    return jsonify(countries), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = next((c for c in preloaded_countries if c.code == country_code), None)
    if not country:
        return jsonify({'error': 'Country not found'}), 404
    return jsonify(country), 200

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    if not is_valid_country_code(country_code):
        return jsonify({'error': 'Invalid country code'}), 400
    cities = [city for city in data_manager.storage.get('City', {}).values() if city.country.code == country_code]
    return jsonify(cities), 200

@app.route('/cities', methods=['POST'])
def create_city():
    try:
        data = request.get_json()
        name = data.get('name')
        country_code = data.get('country_code')

        if not (is_non_empty_string(name) and is_valid_country_code(country_code)):
            return jsonify({'error': 'Invalid input data'}), 400

        if any(city.name == name and city.country.code == country_code for city in data_manager.storage.get('City', {}).values()):
            return jsonify({'error': 'City name already exists in the specified country'}), 409

        country = next(c for c in preloaded_countries if c.code == country_code)
        city = City(name=name, country=country)
        data_manager.save(city)
        return jsonify(city), 201
    except Exception as e:
        logging.exception("Error creating city")
        return jsonify({'error': str(e)}), 500

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = [city for city in data_manager.storage.get('City', {}).values()]
    return jsonify(cities), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    try:
        city = data_manager.get(city_id, 'City')
        if not city:
            return jsonify({'error': 'City not found'}), 404
        return jsonify(city), 200
    except Exception as e:
        logging.exception("Error getting city")
        return jsonify({'error': str(e)}), 500

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    try:
        data = request.get_json()
        city = data_manager.get(city_id, 'City')
        if not city:
            return jsonify({'error': 'City not found'}), 404

        name = data.get('name')
        country_code = data.get('country_code')

        if not (is_non_empty_string(name) and is_valid_country_code(country_code)):
            return jsonify({'error': 'Invalid input data'}), 400

        if any(c.name == name and c.country.code == country_code and c.id != city_id for c in data_manager.storage.get('City', {}).values()):
            return jsonify({'error': 'City name already exists in the specified country'}), 409

        country = next(c for c in preloaded_countries if c.code == country_code)
        city.name = name
        city.country = country
        city.updated_at = datetime.now()
        data_manager.update(city)
        return jsonify(city), 200
    except Exception as e:
        logging.exception("Error updating city")
        return jsonify({'error': str(e)}), 500

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    try:
        city = data_manager.get(city_id, 'City')
        if not city:
            return jsonify({'error': 'City not found'}), 404

        data_manager.delete(city_id, 'City')
        return '', 204
    except Exception as e:
        logging.exception("Error deleting city")
        return jsonify({'error': str(e)}), 500

# User Management Endpoints
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')  # Add password to the user creation

        if not email or not is_valid_email(email):
            return jsonify({"error": "Invalid or missing email"}), 400
        if not first_name or not isinstance(first_name, str):
            return jsonify({"error": "Invalid or missing first name"}), 400
        if not last_name or not isinstance(last_name, str):
            return jsonify({"error": "Invalid or missing last name"}), 400
        if not password or not isinstance(password, str):  # Validate password
            return jsonify({"error": "Invalid or missing password"}), 400

        existing_user = next((user for user in data_manager.storage.get('User', {}).values() if user.email == email), None)
        if existing_user:
            return jsonify({"error": "Email already exists"}), 409

        user = User(email=email, first_name=first_name, last_name=last_name, password=password)  # Include password
        data_manager.save(user)
        return jsonify(user), 201
    except Exception as e:
        logging.exception("Error creating user")
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = [user for user in data_manager.storage.get('User', {}).values()]
        return jsonify(users), 200
    except Exception as e:
        logging.exception("Error getting users")
        return jsonify({'error': str(e)}), 500

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = data_manager.get(user_id, 'User')
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        logging.exception("Error getting user")
        return jsonify({'error': str(e)}), 500

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = data_manager.get(user_id, 'User')
        if not user:
            return jsonify({"error": "User not found"}), 404

        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')  # Add password to the update

        if email and not is_valid_email(email):
            return jsonify({"error": "Invalid email"}), 400
        if first_name and not isinstance(first_name, str):
            return jsonify({"error": "Invalid first name"}), 400
        if last_name and not isinstance(last_name, str):
            return jsonify({"error": "Invalid last name"}), 400
        if password and not isinstance(password, str):  # Validate password
            return jsonify({"error": "Invalid password"}), 400

        if email and email != user.email:
            existing_user = next((u for u in data_manager.storage.get('User', {}).values() if u.email == email), None)
            if existing_user:
                return jsonify({"error": "Email already exists"}), 409

        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if password:  # Update password if provided
            user.password = password
        user.updated_at = datetime.now()
        data_manager.update(user)
        return jsonify(user), 200
    except Exception as e:
        logging.exception("Error updating user")
        return jsonify({'error': str(e)}), 500

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = data_manager.get(user_id, 'User')
        if not user:
            return jsonify({"error": "User not found"}), 404

        data_manager.delete(user_id, 'User')
        return '', 204
    except Exception as e:
        logging.exception("Error deleting user")
        return jsonify({'error': str(e)}), 500

# Amenity Management Endpoints
@app.route('/amenities', methods=['POST'])
def create_amenity():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')  # Add description to amenity creation

        if not is_non_empty_string(name) or not is_non_empty_string(description):
            return jsonify({'error': 'Invalid input data'}), 400

        if any(amenity.name == name for amenity in data_manager.storage.get('Amenity', {}).values()):
            return jsonify({'error': 'Amenity name already exists'}), 409

        amenity = Amenity(name=name, description=description)  # Include description
        data_manager.save(amenity)
        return jsonify(amenity), 201
    except Exception as e:
        logging.exception("Error creating amenity")
        return jsonify({'error': str(e)}), 500

@app.route('/amenities', methods=['GET'])
def get_amenities():
    try:
        amenities = [amenity for amenity in data_manager.storage.get('Amenity', {}).values()]
        return jsonify(amenities), 200
    except Exception as e:
        logging.exception("Error getting amenities")
        return jsonify({'error': str(e)}), 500

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    try:
        amenity = data_manager.get(amenity_id, 'Amenity')
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404
        return jsonify(amenity), 200
    except Exception as e:
        logging.exception("Error getting amenity")
        return jsonify({'error': str(e)}), 500

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    try:
        data = request.get_json()
        amenity = data_manager.get(amenity_id, 'Amenity')
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404

        name = data.get('name')
        description = data.get('description')  # Add description to the update

        if not is_non_empty_string(name) or not is_non_empty_string(description):
            return jsonify({'error': 'Invalid input data'}), 400

        if any(a.name == name and a.id != amenity_id for a in data_manager.storage.get('Amenity', {}).values()):
            return jsonify({'error': 'Amenity name already exists'}), 409

        amenity.name = name
        amenity.description = description  # Update description
        amenity.updated_at = datetime.now()
        data_manager.update(amenity)
        return jsonify(amenity), 200
    except Exception as e:
        logging.exception("Error updating amenity")
        return jsonify({'error': str(e)}), 500

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    try:
        amenity = data_manager.get(amenity_id, 'Amenity')
        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404

        data_manager.delete(amenity_id, 'Amenity')
        return '', 204
    except Exception as e:
        logging.exception("Error deleting amenity")
        return jsonify({'error': str(e)}), 500

# Review Management Endpoints
@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        rating = data.get('rating')
        comment = data.get('comment')

        place = data_manager.get(place_id, 'Place')
        user = data_manager.get(user_id, 'User')

        if not (place and user):
            return jsonify({'error': 'Invalid place or user ID'}), 400

        if user_id == place.host.id:
            return jsonify({'error': 'Hosts cannot review their own places'}), 400

        if not is_valid_rating(rating):
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400

        review = Review(place=place, user=user, rating=rating, comment=comment)
        data_manager.save(review)
        return jsonify(review), 201
    except Exception as e:
        logging.exception("Error creating review")
        return jsonify({'error': str(e)}), 500

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    try:
        user = data_manager.get(user_id, 'User')
        if not user:
            return jsonify({'error': 'User not found'}), 404
        reviews = [review for review in data_manager.storage.get('Review', {}).values() if review.user.id == user_id]
        return jsonify(reviews), 200
    except Exception as e:
        logging.exception("Error getting reviews by user")
        return jsonify({'error': str(e)}), 500

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    try:
        place = data_manager.get(place_id, 'Place')
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        reviews = [review for review in data_manager.storage.get('Review', {}).values() if review.place.id == place_id]
        return jsonify(reviews), 200
    except Exception as e:
        logging.exception("Error getting reviews by place")
        return jsonify({'error': str(e)}), 500

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    try:
        review = data_manager.get(review_id, 'Review')
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        return jsonify(review), 200
    except Exception as e:
        logging.exception("Error getting review")
        return jsonify({'error': str(e)}), 500

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    try:
        data = request.get_json()
        review = data_manager.get(review_id, 'Review')
        if not review:
            return jsonify({'error': 'Review not found'}), 404

        rating = data.get('rating')
        comment = data.get('comment')

        if not is_valid_rating(rating):
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400

        review.rating = rating
        review.comment = comment
        review.updated_at = datetime.now()
        data_manager.update(review)
        return jsonify(review), 200
    except Exception as e:
        logging.exception("Error updating review")
        return jsonify({'error': str(e)}), 500

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        review = data_manager.get(review_id, 'Review')
        if not review:
            return jsonify({'error': 'Review not found'}), 404

        data_manager.delete(review_id, 'Review')
        return '', 204
    except Exception as e:
        logging.exception("Error deleting review")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
