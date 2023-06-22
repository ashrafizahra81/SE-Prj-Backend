from abc import ABC, abstractmethod

class UserService(ABC):

    @abstractmethod
    def updateUser(self, serialized_data, is_valid):
        pass
    @abstractmethod
    def updateUserScore(self , score , email):
        pass
    @abstractmethod
    def updateUserIsValid(self, user, is_valid):
        pass
    @abstractmethod
    def updateUserPassword(self, email, password):
        pass
    @abstractmethod
    def updateUserCode(self, user, code):
        pass