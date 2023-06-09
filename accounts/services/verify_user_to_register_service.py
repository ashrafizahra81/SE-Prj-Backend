from ..models import User, CodesForUsers
from .verify_user_to_register_interface import VerfyUserToResgisterService
from rest_framework_simplejwt.tokens import RefreshToken
from Backend import dependencies
import logging

logger = logging.getLogger("django")


class ConcreteVerfyUserToResgisterService(VerfyUserToResgisterService):

    def verify_user_to_register(self, code):

        userCode = CodesForUsers.objects.get(code = int(code))
        logger.info('code for user with email '+ userCode.email+' deleted')
        user = User.objects.get(email = userCode.email)
        CodesForUsers.objects.filter(code=int(code)).delete()
        dependencies.user_service_instance.updateUserIsValid(user, 1)
        logger.info('User with email '+ user.email+' is active now')
        data={}
        if(user.shop_name == None):
            logger.info('The user is a customer')
            data['username'] = user.username
            data['email'] = user.email
            data['user_phone_number'] = user.user_phone_number
            data['balance'] = 0
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['score'] = 0
            data['type'] = "user"
        else:
            logger.info('The user is a seller')
            data['username'] = user.username
            data['email'] = user.email
            data['shop_name'] = user.shop_name
            data['shop_address'] = user.shop_address
            data['shop_phone_number'] = user.shop_phone_number
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['type'] = "seller"
        logger.info('The user is active now')
        
        return data