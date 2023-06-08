from abc import ABC, abstractmethod



class CodeForUsersService(ABC):
    
    @abstractmethod
    def updateCodesForUsers(self, token, email, date):
        pass

    @abstractmethod
    def createCodesForUsers(self, token, email, date):
        pass

    