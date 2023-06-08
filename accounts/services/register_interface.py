from abc import ABC, abstractmethod

class RegisterService(ABC):

    @abstractmethod
    def userRegister(self, email):
        pass
