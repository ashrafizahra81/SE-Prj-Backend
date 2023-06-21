from abc import ABC, abstractmethod

class ResetPasswordService(ABC):

    @abstractmethod
    def reset_password(self, request):
        pass

    @abstractmethod
    def update_user_code(self, userId):
        pass