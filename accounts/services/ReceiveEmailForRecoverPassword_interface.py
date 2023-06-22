from abc import ABC, abstractmethod

class ReceiveEmailForRecoverPasswordService(ABC):

    @abstractmethod
    def receiveEmailForRecoverPassword(self, email):

        pass