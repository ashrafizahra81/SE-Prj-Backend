from abc import ABC, abstractmethod

class GetGiftService(ABC):

    @abstractmethod
    def get_gifts(self, user, score):
        pass