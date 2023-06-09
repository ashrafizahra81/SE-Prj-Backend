from abc import ABC, abstractmethod

class ShowUserInfoService(ABC):

    @abstractmethod
    def show_user_info(self, user_id):
        pass