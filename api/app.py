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

if __name__ == "__main__":
    app.run(debug=True)
