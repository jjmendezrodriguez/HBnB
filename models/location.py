import uuid
from datetime import datetime

class Country:
    def __init__(self, name):
        self.name = name

class City:
    def __init__(self, name, country):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country = country
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
