from abc import ABC, abstractmethod  # Import ABC and abstractmethod for defining abstract base classes

class IPersistenceManager(ABC):
    """
    Interface for persistence manager to handle CRUD operations for various entities.
    """
    
    @abstractmethod
    def save(self, entity):
        """
        Save an entity to the storage.

        Args:
            entity (object): The entity to save.
        """
        pass

    @abstractmethod
    def get(self, entity_id, entity_type):
        """
        Retrieve an entity from the storage.

        Args:
            entity_id (str): The ID of the entity to retrieve.
            entity_type (str): The type of the entity to retrieve.

        Returns:
            object: The retrieved entity.
        """
        pass

    @abstractmethod
    def update(self, entity):
        """
        Update an entity in the storage.

        Args:
            entity (object): The entity to update.
        """
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        """
        Delete an entity from the storage.

        Args:
            entity_id (str): The ID of the entity to delete.
            entity_type (str): The type of the entity to delete.
        """
        pass
