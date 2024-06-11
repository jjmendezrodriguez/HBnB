# persistence/__init__.py

# Import the persistence manager interface
from .i_persistence_manager import IPersistenceManager
# Import the DataManager class, which implements the IPersistenceManager interface
from .data_manager import DataManager
# Import the FileStorage class for file-based data storage
from .file_storage import FileStorage

"""This file ensures that the persistence-related classes are accessible when the persistence package is imported.
This allows for easy importing of these classes throughout the application."""
