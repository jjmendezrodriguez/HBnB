import json
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.location import Country, City

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def save(self):
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(FileStorage.__objects, f, default=lambda o: o.__dict__)

    def reload(self):
        try:
            with open(FileStorage.__file_path, 'r') as f:
                FileStorage.__objects = json.load(f)
        except FileNotFoundError:
            pass
