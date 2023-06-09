from abc import ABC, abstractmethod

class VerfyUserToResgisterService(ABC):

    @abstractmethod
    def verify_user_to_register(self, code):
        pass
