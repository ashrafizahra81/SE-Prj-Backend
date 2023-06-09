from .wallet_interface import WalletService
from ..models import Wallet

class ConcreteWalletService(WalletService):

    def createWallet(self, user, balance):

        wallet = Wallet(
            user = user,
            balance = 0, 
        )
        wallet.save()
    
    def updateWallet(self, user, insert):
        wallet = Wallet.objects.get(user=user)
        wallet.balance += float(insert)
        wallet.save()