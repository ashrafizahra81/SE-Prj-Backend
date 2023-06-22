from .ReceiveEmailForRecoverPassword_interface import ReceiveEmailForRecoverPasswordService
from ..models import User
from Backend import dependencies
import logging

logger = logging.getLogger("django")

class ConcreteReceiveEmailForRecoverPasswordService(ReceiveEmailForRecoverPasswordService):

    def receiveEmailForRecoverPassword(self, email):
        
        logger.info('request recieved from POST /accounts/receive_email_for_recover_password/')

        user = User.objects.get(email=email)
        token1 = dependencies.mail_service_instance.propareEmailBody(user.email)
        return token1