from abc import ABC , abstractmethod

class RegistrationFactory(ABC):

    @abstractmethod
    def create_viewset(self):
        pass

    @abstractmethod
    def create_serializer(self):
        pass