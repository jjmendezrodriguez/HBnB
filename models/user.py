import uuid  # Import the uuid module to generate unique identifiers
from datetime import datetime  # Import the datetime module to handle date and time

class User:
    """
    Represents a user in the HBnB system.
    
    Attributes:
        id (str): Unique identifier for the user.
        email (str): Email of the user.
        password (str): Password of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
    """
    
    def __init__(self, email, password, first_name, last_name, id=None):
        """
        Initializes a new User instance.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            id (str, optional): Unique identifier for the user. If not provided, a new UUID will be generated.
        """
        self.id = id or str(uuid.uuid4())  # Generate a unique ID for the user if not provided
        self.email = email  # Set the email of the user
        self.password = password  # Set the password of the user
        self.first_name = first_name  # Set the first name of the user
        self.last_name = last_name  # Set the last name of the user
        self.created_at = datetime.now()  # Set the creation timestamp
        self.updated_at = datetime.now()  # Set the last updated timestamp
