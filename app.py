from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.location import Country, City
from datetime import datetime
import re

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

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = [country.__dict__ for country in preloaded_countries]
    return jsonify(countries), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = next((c for c in preloaded_countries if c.code == country_code), None)
    if not country:
        return jsonify({'error': 'Country not found'}), 404
    return jsonify(country.__dict__), 200

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    if not is_valid_country_code(country_code):
        return jsonify({'error': 'Invalid country code'}), 400
    cities = [city.__dict__ for city in data_manager.storage.get('City', {}).values() if city.country.code == country_code]
    return jsonify(cities), 200

@app.route('/cities', methods=['POST'])
def create_city():
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
    return jsonify(city.__dict__), 201

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = [city.__dict__ for city in data_manager.storage.get('City', {}).values()]
    return jsonify(cities), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({'error': 'City not found'}), 404
    return jsonify(city.__dict__), 200

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
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
    return jsonify(city.__dict__), 200

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({'error': 'City not found'}), 404

    data_manager.delete(city_id, 'City')
    return '', 204

# Places Management Endpoints

def is_valid_latitude(lat):
    return isinstance(lat, (int, float)) and -90 <= lat <= 90

def is_valid_longitude(lon):
    return isinstance(lon, (int, float)) and -180 <= lon <= 180

def is_non_negative_integer(value):
    return isinstance(value, int) and value >= 0

def validate_place_data(data):
    required_fields = ["name", "description", "address", "city_id", "latitude", "longitude", "host_id", "number_of_rooms", "number_of_bathrooms", "price_per_night", "max_guests", "amenity_ids"]
    if not all(field in data for field in required_fields):
        return False

    if not is_non_negative_integer(data["number_of_rooms"]) or not is_non_negative_integer(data["number_of_bathrooms"]) or not is_non_negative_integer(data["max_guests"]):
        return False

    if not is_valid_latitude(data["latitude"]) or not is_valid_longitude(data["longitude"]):
        return False

    return True

@app.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()

    if not validate_place_data(data):
        return jsonify({'error': 'Invalid input data'}), 400

    if not data_manager.get(data['city_id'], 'City'):
        return jsonify({'error': 'City not found'}), 404
   
# Check if amenity IDs exist in the database
    for amenity_id in data['amenity_ids']:
        if not data_manager.get(amenity_id, 'Amenity'):
            return jsonify({'error': f'Amenity ID {amenity_id} not found'}), 404

    place = Place(**data)
    data_manager.save(place)
    return jsonify(place.__dict__), 201

@app.route('/places', methods=['GET'])
def get_places():
    places = [place.__dict__ for place in data_manager.storage.get('Place', {}).values()]
    for place in places:
        city = data_manager.get(place['city_id'], 'City')
        if city:
            place['city'] = city.__dict__
        amenities = [data_manager.get(aid, 'Amenity').__dict__ for aid in place['amenity_ids']]
        place['amenities'] = amenities
    return jsonify(places), 200

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    place_data = place.__dict__.copy()
    city = data_manager.get(place.city_id, 'City')
    if city:
        place_data['city'] = city.__dict__
    amenities = [data_manager.get(aid, 'Amenity').__dict__ for aid in place.amenity_ids]
    place_data['amenities'] = amenities

    return jsonify(place_data), 200

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json()
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    if not validate_place_data(data):
        return jsonify({'error': 'Invalid input data'}), 400

    if not data_manager.get(data['city_id'], 'City'):
        return jsonify({'error': 'City not found'}), 404

    for amenity_id in data['amenity_ids']:
        if not data_manager.get(amenity_id, 'Amenity'):
            return jsonify({'error': f'Amenity ID {amenity_id} not found'}), 404

    for key, value in data.items():
        setattr(place, key, value)
    place.updated_at = datetime.now()
    data_manager.update(place)

    return jsonify(place.__dict__), 200

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data_manager.delete(place_id, 'Place')
    return '', 204    

# User Management Endpoints
users = {}
user_id_counter = 1

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None

def find_user_by_email(email):
    return next((user for user in users.values() if user['email'] == email), None)

@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    # Validate input
    if not email or not is_valid_email(email):
        return jsonify({"error": "Invalid or missing email"}), 400
    if not first_name or not isinstance(first_name, str):
        return jsonify({"error": "Invalid or missing first name"}), 400
    if not last_name or not isinstance(last_name, str):
        return jsonify({"error": "Invalid or missing last name"}), 400
    
    # Check for unique email
    if find_user_by_email(email):
        return jsonify({"error": "Email already exists"}), 409

    user = {
        "id": user_id_counter,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    users[user_id_counter] = user
    user_id_counter += 1
    
    return jsonify(user), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    # Validate input
    if email and not is_valid_email(email):
        return jsonify({"error": "Invalid email"}), 400
    if first_name and not isinstance(first_name, str):
        return jsonify({"error": "Invalid first name"}), 400
    if last_name and not isinstance(last_name, str):
        return jsonify({"error": "Invalid last name"}), 400
    
    # Check for unique email if changed
    if email and email != user['email'] and find_user_by_email(email):
        return jsonify({"error": "Email already exists"}), 409
    
    # Update user fields
    if email:
        user['email'] = email
    if first_name:
        user['first_name'] = first_name
    if last_name:
        user['last_name'] = last_name
    user['updated_at'] = datetime.utcnow().isoformat()
    
    return jsonify(user), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = users.pop(user_id, None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)

