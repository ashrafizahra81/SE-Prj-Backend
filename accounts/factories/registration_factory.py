from abc import ABC , abstractmethod

class RegistrationFactory(ABC):

    @abstractmethod
    def create_viewset(self):
        pass