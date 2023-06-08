from abc import ABC, abstractmethod

class WalletService(ABC):

    @abstractmethod
    def createWallet(self, user, balance):
        pass