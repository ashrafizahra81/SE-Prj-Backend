from .resetPassword_interface import ResetPasswordService
from rest_framework.response import Response
from rest_framework import status
from Backend import dependencies
from ..models import User

import logging

logger = logging.getLogger("django")

class ConcreteResetPasswordService(ResetPasswordService):

    def reset_password(self, request):
        
        logger.info('request recieved from POST /accounts/reset_password/')
        data2 = request.data
        token_recieved=data2['token']
        password=data2['password']
        password_again=data2['password2']
        used = User.objects.get(id=request.user.id)
        if int(token_recieved) !=used.random_integer:
            logger.warn('token entered '+str(token_recieved)+' is not equal with '+str(used.random_integer))
            return Response({'message':'Invalid Token'} , status=status.HTTP_400_BAD_REQUEST)

        if password!=password_again:
            logger.warn('password_again '+password_again+' is not equal with password'+password)
            return Response({'message':'Passwords should match'} , status=status.HTTP_400_BAD_REQUEST)

        dependencies.user_service_instance.updateUserPassword(used, password)

        logger.info('password of user '+str(used.pk)+' changed successfuly')
        return Response('Password changed successfully')
    
    def update_user_code(self, userId):
        
        logger.info('request recieved from GET /accounts/reset_password/')
        used=User.objects.get(id=userId)
        token1 = dependencies.mail_service_instance.sendEmail(used.email)
        dependencies.user_service_instance.updateUserCode(used,token1)

