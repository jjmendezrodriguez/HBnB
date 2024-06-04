import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name, description):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
