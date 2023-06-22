from abc import ABC, abstractmethod

class RegisterService(ABC):

    @abstractmethod
    def userRegister(self, email):
        pass

class CheckEmailForRegister(ABC):

    @abstractmethod
    def checkIfEmailExists(self, email):
        pass

class SaveNewUser(ABC):

    @abstractmethod
    def saveNewUser(self, serialized_data, email, phone_number):
        pass
