import uuid  # Import the uuid module to generate unique identifiers
from datetime import datetime  # Import the datetime module to handle date and time

class Review:
    """
    Represents a review in the HBnB system.
    
    Attributes:
        id (str): Unique identifier for the review.
        user_id (str): Identifier for the user who wrote the review.
        place_id (str): Identifier for the place being reviewed.
        rating (int): Rating given to the place.
        comment (str): Comment about the place.
        created_at (datetime): Timestamp when the review was created.
        updated_at (datetime): Timestamp when the review was last updated.
    """
    
    def __init__(self, user_id, place_id, rating, comment, id=None):
        """
        Initializes a new Review instance.

        Args:
            user_id (str): Identifier for the user who wrote the review.
            place_id (str): Identifier for the place being reviewed.
            rating (int): Rating given to the place.
            comment (str): Comment about the place.
            id (str, optional): Unique identifier for the review. If not provided, a new UUID will be generated.
        """
        self.id = id or str(uuid.uuid4())  # Generate a unique ID for the review if not provided
        self.user_id = user_id  # Set the user ID who wrote the review
        self.place_id = place_id  # Set the place ID being reviewed
        self.rating = rating  # Set the rating given to the place
        self.comment = comment  # Set the comment about the place
        self.created_at = datetime.now()  # Set the creation timestamp
        self.updated_at = datetime.now()  # Set the last updated timestamp
