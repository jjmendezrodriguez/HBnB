import uuid  # Import the uuid module to generate unique identifiers
from datetime import datetime  # Import the datetime module to handle date and time

class Place:
    """
    Represents a place in the HBnB system.
    
    Attributes:
        id (str): Unique identifier for the place.
        name (str): Name of the place.
        description (str): Description of the place.
        city_id (str): Identifier for the city where the place is located.
        host_id (str): Identifier for the host of the place.
        latitude (float): Latitude of the place.
        longitude (float): Longitude of the place.
        price_per_night (float): Price per night for the place.
        max_guests (int): Maximum number of guests allowed.
        number_of_rooms (int): Number of rooms in the place.
        number_of_bathrooms (int): Number of bathrooms in the place.
        amenity_ids (list): List of amenity identifiers associated with the place.
        created_at (datetime): Timestamp when the place was created.
        updated_at (datetime): Timestamp when the place was last updated.
    """
    
    def __init__(self, name, description, city_id, host_id, latitude, longitude, price_per_night, max_guests, number_of_rooms, number_of_bathrooms, amenity_ids):
        """
        Initializes a new Place instance.

        Args:
            name (str): Name of the place.
            description (str): Description of the place.
            city_id (str): Identifier for the city where the place is located.
            host_id (str): Identifier for the host of the place.
            latitude (float): Latitude of the place.
            longitude (float): Longitude of the place.
            price_per_night (float): Price per night for the place.
            max_guests (int): Maximum number of guests allowed.
            number_of_rooms (int): Number of rooms in the place.
            number_of_bathrooms (int): Number of bathrooms in the place.
            amenity_ids (list): List of amenity identifiers associated with the place.
        """
        self.id = str(uuid.uuid4())  # Generate a unique ID for the place
        self.name = name  # Set the name of the place
        self.description = description  # Set the description of the place
        self.city_id = city_id  # Set the city ID where the place is located
        self.host_id = host_id  # Set the host ID of the place
        self.latitude = latitude  # Set the latitude of the place
        self.longitude = longitude  # Set the longitude of the place
        self.price_per_night = price_per_night  # Set the price per night for the place
        self.max_guests = max_guests  # Set the maximum number of guests allowed
        self.number_of_rooms = number_of_rooms  # Set the number of rooms in the place
        self.number_of_bathrooms = number_of_bathrooms  # Set the number of bathrooms in the place
        self.amenity_ids = amenity_ids  # Set the list of amenity IDs associated with the place
        self.created_at = datetime.now()  # Set the creation timestamp
        self.updated_at = datetime.now()  # Set the last updated timestamp
