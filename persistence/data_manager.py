import json
from .i_persistence_manager import IPersistenceManager
from models.location import Country

class DataManager(IPersistenceManager):
    def __init__(self):
        self.storage = {}
        self._load_from_file()

    def save(self, entity):
        entity_type = type(entity).__name__
        if entity_type not in self.storage:
            self.storage[entity_type] = {}
        if hasattr(entity, 'id'):
            entity_id = entity.id
        else:
            entity_id = len(self.storage[entity_type]) + 1
            setattr(entity, 'id', entity_id)
            self.storage[entity_type][entity_id] = entity
            self._save_to_file()

    def get(self, entity_id, entity_type):
        return self.storage.get(entity_type, {}).get(entity_id)

    def update(self, entity):
        entity_type = type(entity).__name__
        if entity_type in self.storage:
            self.storage[entity_type][entity.id] = entity
            self._save_to_file()

    def delete(self, entity_id, entity_type):
        if entity_type in self.storage and entity_id in self.storage[entity_type]:
            del self.storage[entity_type][entity_id]
            self._save_to_file()

    def _save_to_file(self):
        with open('storage.json', 'w') as f:
            json.dump({k: {eid: e.__dict__ for eid, e in v.items()} for k, v in self.storage.items()}, f)

    def _load_from_file(self):
        try:
            with open('storage.json', 'r') as f:
                data = json.load(f)
                self.storage = {k: {eid: self._reconstruct_entity(k, e) for eid, e in v.items()} for k, v in data.items()}
        except FileNotFoundError:
            pass

    def _reconstruct_entity(self, entity_type, entity_data):
        cls = globals()[entity_type]
        entity = cls.__new__(cls)
        entity.__dict__.update(entity_data)
        return entity
