from abc import ABC, abstractmethod

class ChargeWalletService(ABC):

    @abstractmethod
    def check_money_in_wallet(self, insert):
        pass
