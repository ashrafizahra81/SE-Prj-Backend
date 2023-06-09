from .show_user_info_interface import ShowUserInfoService
from ..models import User
from wallets.models import Wallet
import logging

logger = logging.getLogger("django")

class ConcreteShowUserInfoService(ShowUserInfoService):

    def show_user_info(self, user_id):
        
        userObj = User.objects.get(id=user_id)
        logger.info('user '+str(userObj.pk)+ ' is a customer')
        data = {}
        data['email'] = userObj.email
        data['username'] = userObj.username
        data['user_phone_number'] = userObj.user_phone_number
        data['user_postal_code'] = userObj.user_postal_code
        data['user_address'] = userObj.user_address
        wallet = Wallet.objects.get(user = userObj)
        data['inventory'] = wallet.balance

        return data
    


class ConcreteShowShopManagerInfoService(ShowUserInfoService):

    def show_user_info(self, user_id):

        userObj = User.objects.get(id=user_id)
        logger.info('user '+str(userObj.pk)+ ' is a seller')

        data = {}
        data['email'] = userObj.email
        data['username'] = userObj.username
        data['shop_name'] = userObj.shop_name
        data['shop_phone_number'] = userObj.shop_phone_number
        data['user_phone_number'] = userObj.user_phone_number
        data['shop_address'] = userObj.shop_address

        return data
