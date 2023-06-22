from abc import ABC , abstractmethod

class EditFactory(ABC):

    @abstractmethod
    def create_viewset(self):
        pass