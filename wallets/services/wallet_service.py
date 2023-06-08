from .wallet_interface import WalletService
from ..models import Wallet

class ConcreteWalletService(WalletService):

    def createWallet(self, user, balance):

        wallet = Wallet(
            user = user,
            balance = 0, 
        )
        wallet.save()