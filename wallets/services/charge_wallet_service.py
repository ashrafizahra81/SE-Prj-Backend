from .charge_wallet_interface import ChargeWalletService
import logging
logger = logging.getLogger("django")

class ConcreteChargeWalletService(ChargeWalletService):

    def check_money_in_wallet(self, insert):
        
        data = {}
        print(insert == '')
        if(insert == '' or int(insert) < 0 or int(insert) == 0):
            logger.warn('data entered is invalid')
            data={"message": "مقدار وارد شده قابل قبول نیست"}
            return data
