from .register_interface import RegisterService
import logging
from accounts.models import *
from datetime import datetime
from Backend import dependencies

user_service_instance = dependencies.user_service_instance
wallet_service_instance = dependencies.wallet_service_instance



logger = logging.getLogger("django")

mail_service_instance = dependencies.mail_service_instance
codeForUsers_service_instance = dependencies.codeForUsers_service_instance

class ConcreteUserRegisterServiceForExistedUser(RegisterService):

    def userRegister(self, serialized_data):

        logger.info('This email already exists: ' + serialized_data.data['email'])

        userCode = CodesForUsers.objects.get(email = serialized_data.data['email'])
        now = datetime.now()
        delta = now - userCode.created_at.replace(tzinfo=None)
        diff = delta.seconds
        token = mail_service_instance.sendEmail(userCode.email)
        codeForUsers_service_instance.updateCodesForUsers(token, serialized_data.data['email'], datetime.now())
        logger.info('The code stored in database for user '+userCode.email)
    
class ConcreteUserRegisterServiceForNewUser(RegisterService):

    def userRegister(self, serialized_data):

        user_service_instance.updateUser(serialized_data, 0)
        token = mail_service_instance.sendEmail(serialized_data.data['email'])
        codeForUsers_service_instance.createCodesForUsers(token, serialized_data.data['email'], datetime.now())

        account = User.objects.get(email = serialized_data.data['email'])
        wallet_service_instance.createWallet(account, 0)

        logger.info('User ' + str(account.pk)+ ' and its code stored in database')
        

