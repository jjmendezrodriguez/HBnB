import uuid  # Import the uuid module to generate unique identifiers
from datetime import datetime  # Import the datetime module to handle date and time

class Country:
    """
    Represents a country in the HBnB system.
    
    Attributes:
        id (str): Unique identifier for the country.
        name (str): Name of the country.
        code (str): ISO code of the country.
        created_at (datetime): Timestamp when the country was created.
        updated_at (datetime): Timestamp when the country was last updated.
    """
    
    def __init__(self, name, code):
        """
        Initializes a new Country instance.

        Args:
            name (str): Name of the country.
            code (str): ISO code of the country.
        """
        self.id = str(uuid.uuid4())  # Generate a unique ID for the country
        self.name = name  # Set the name of the country
        self.code = code  # Set the ISO code of the country
        self.created_at = datetime.now()  # Set the creation timestamp
        self.updated_at = datetime.now()  # Set the last updated timestamp

class City:
    """
    Represents a city in the HBnB system.
    
    Attributes:
        id (str): Unique identifier for the city.
        name (str): Name of the city.
        country_code (str): ISO code of the country the city belongs to.
        created_at (datetime): Timestamp when the city was created.
        updated_at (datetime): Timestamp when the city was last updated.
    """
    
    def __init__(self, name, country_code, id=None):
        """
        Initializes a new City instance.

        Args:
            name (str): Name of the city.
            country_code (str): ISO code of the country the city belongs to.
            id (str, optional): Unique identifier for the city. If not provided, a new UUID will be generated.
        """
        self.id = id or str(uuid.uuid4())  # Generate a unique ID for the city if not provided
        self.name = name  # Set the name of the city
        self.country_code = country_code  # Set the country code of the city
        self.created_at = datetime.now()  # Set the creation timestamp
        self.updated_at = datetime.now()  # Set the last updated timestamp
