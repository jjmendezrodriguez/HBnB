import uuid
from datetime import datetime

class Amenity:
    """
    Represents an amenity in the HBnB system.
    
    Attributes:
        id (str): Unique identifier for the amenity.
        name (str): Name of the amenity.
        description (str): Description of the amenity.
        created_at (datetime): Timestamp when the amenity was created.
        updated_at (datetime): Timestamp when the amenity was last updated.
    """
    
    def __init__(self, name, description):
        """
        Initializes a new Amenity instance.

        Args:
            name (str): Name of the amenity.
            description (str): Description of the amenity.
        """
        self.id = str(uuid.uuid4())  # Generate a unique ID for the amenity
        self.name = name  # Set the name of the amenity
        self.description = description  # Set the description of the amenity
        self.created_at = datetime.now()  # Set the creation timestamp
        self.updated_at = datetime.now()  # Set the last updated timestamp
