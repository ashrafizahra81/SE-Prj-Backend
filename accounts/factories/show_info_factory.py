from abc import ABC , abstractmethod

class ShowInfoFactory(ABC):

    @abstractmethod
    def create_viewset(self):
        pass