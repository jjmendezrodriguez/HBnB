# models/__init__.py

# Import the Amenity model class
from .amenity import Amenity

# Import the Country and City model classes from the location module
from .location import Country, City

# Import the Place model class
from .place import Place

# Import the Review model class
from .review import Review

# Import the User model class
from .user import User

"""This file ensures that all the model classes are accessible when the models package is imported.
This allows for easy importing of the model classes throughout the application."""
