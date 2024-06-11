import json  # Import the json module to handle JSON data
from datetime import datetime  # Import the datetime module to handle date and time
from .i_persistence_manager import IPersistenceManager  # Import the persistence manager interface

class DataManager(IPersistenceManager):
    """
    DataManager class implementing the IPersistenceManager interface
    to handle CRUD operations for various entities.
    """
    
    def __init__(self, storage_file='storage.json'):
        """
        Initializes a new DataManager instance.

        Args:
            storage_file (str): The file path for the storage file.
        """
        self.storage_file = storage_file  # Set the path for the storage file
        self._load_storage()  # Load storage data from the storage file

    def _load_storage(self):
        """Loads storage data from the storage file."""
        try:
            with open(self.storage_file, 'r') as f:
                self.storage = json.load(f)  # Load JSON data from the file into the storage attribute
                # Ensure all values are lists
                for key in self.storage:
                    if not isinstance(self.storage[key], list):
                        self.storage[key] = []
        except FileNotFoundError:
            self.storage = {}  # If the file is not found, initialize an empty storage dictionary

    def _save_storage(self):
        """Saves storage data to the storage file."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.storage, f, default=str)  # Write the storage data as JSON to the file

    def save(self, entity):
        """
        Save an entity to the storage.

        Args:
            entity (object): The entity to save.
        """
        entity_type = type(entity).__name__  # Get the type name of the entity
        if entity_type not in self.storage:
            self.storage[entity_type] = []  # Initialize the list for this entity type if it doesn't exist
        elif not isinstance(self.storage[entity_type], list):
            self.storage[entity_type] = []  # Ensure it is a list
        self.storage[entity_type].append(entity.__dict__)  # Add the entity's dictionary representation to the storage
        self._save_storage()  # Save the updated storage data to the file

    def get(self, entity_id, entity_type):
        """
        Retrieve an entity from the storage.

        Args:
            entity_id (str): The ID of the entity to retrieve.
            entity_type (str): The type of the entity to retrieve.

        Returns:
            object: The retrieved entity or None if not found.
        """
        entities = self.storage.get(entity_type, [])  # Get the list of entities of the given type
        for entity in entities:
            if entity['id'] == entity_id:
                return entity  # Return the entity if the ID matches
        return None  # Return None if the entity is not found

    def update(self, entity):
        """
        Update an entity in the storage.

        Args:
            entity (object): The entity to update.
        """
        entity_type = type(entity).__name__  # Get the type name of the entity
        entities = self.storage.get(entity_type, [])  # Get the list of entities of the given type
        for idx, existing_entity in enumerate(entities):
            if existing_entity['id'] == entity.id:
                entities[idx] = entity.__dict__  # Update the entity's dictionary representation in the storage
                self._save_storage()  # Save the updated storage data to the file
                return
        raise ValueError(f"Entity of type {entity_type} with ID {entity.id} not found.")  # Raise an error if the entity is not found

    def delete(self, entity_id, entity_type):
        """
        Delete an entity from the storage.

        Args:
            entity_id (str): The ID of the entity to delete.
            entity_type (str): The type of the entity to delete.
        """
        entities = self.storage.get(entity_type, [])  # Get the list of entities of the given type
        for idx, entity in enumerate(entities):
            if entity['id'] == entity_id:
                entities.pop(idx)  # Remove the entity from the list if the ID matches
                self._save_storage()  # Save the updated storage data to the file
                return
        raise ValueError(f"Entity of type {entity_type} with ID {entity_id} not found.")  # Raise an error if the entity is not found
