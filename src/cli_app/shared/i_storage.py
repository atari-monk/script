from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def load_all(self, model):
        """Load all data and return model instances."""
        pass

    @abstractmethod
    def save_all(self, instances):
        """Save model instances to storage."""
        pass

    @abstractmethod
    def append(self, instance):
        """Appends a model instance to the storage."""
        pass
    