from abc import ABC, abstractmethod

class UserService(ABC):

    @abstractmethod
    def updateUser(self, serialized_data, is_valid):
        pass
    @abstractmethod
    def updateUserScore(self , score , email):
        pass