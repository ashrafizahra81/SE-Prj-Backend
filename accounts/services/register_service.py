from .register_interface import RegisterService, CheckEmailForRegister, SaveNewUser
import logging
from accounts.models import *
from accounts.serializers import *
from datetime import datetime
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status



user_service_instance = dependencies.user_service_instance
wallet_service_instance = dependencies.wallet_service_instance



logger = logging.getLogger("django")

mail_service_instance = dependencies.mail_service_instance
codeForUsers_service_instance = dependencies.codeForUsers_service_instance

class ConcreteUserRegisterServiceForExistedUser(RegisterService):

    def userRegister(self, email):


        
        logger.info('This email already exists: ' +email)

        userCode = CodesForUsers.objects.get(email = email)
        now = datetime.now()
        delta = now - userCode.created_at.replace(tzinfo=None)
        diff = delta.seconds
        token = mail_service_instance.propareEmailBody(userCode.email)
        codeForUsers_service_instance.updateCodesForUsers(token, email, datetime.now())
        logger.info('The code stored in database for user '+userCode.email)
    
class ConcreteUserRegisterServiceForNewUser(RegisterService):

    def userRegister(self, email):

        # user_service_instance.updateUser(serialized_data, 0)
        
        token = mail_service_instance.propareEmailBody(email)
        codeForUsers_service_instance.createCodesForUsers(token, email, datetime.now())

        account = User.objects.get(email = email)
        wallet_service_instance.createWallet(account, 0)

        logger.info('User ' + str(account.pk)+ ' and its code stored in database')
    

class ConcreteCheckEmailForRegister(CheckEmailForRegister):

    def checkIfEmailExists(self, email):

        data = {}
        
        logger.info('This email already exists: ' + email)
        if(User.objects.get(email = email).is_active == 1):
            logger.info('This account is active: ' + email)
            
            data['message'] = "کاربری فعال با این ایمیل یافت شد"
            data['status'] = status.HTTP_400_BAD_REQUEST
            return data
        
        if(codeForUsers_service_instance.hasExpired(email)):
            
            
            dependencies.register_for_existed_user_service_instance.userRegister(email)
            
            data['message'] = "کد جدید به ایمیل ارسال شد"
            data['status'] = status.HTTP_201_CREATED
            
            return data
        
        
        data['message'] = "کد به ایمیل شما ارسال شده است"
        data['status'] = status.HTTP_202_ACCEPTED
        logger.info('User has valid code')
        return data

class ConcreteSaveNewUserService(SaveNewUser):
    
    def saveNewUser(self, serialized_data, email, phone_number):
        logger.info('Data entered is valid')
        if(not(phone_number.isdigit())):
            logger.warn('user_phone_number is invalid')
            data['message'] = "شماره تلفن وارد شده صحیح نیست"
            data['status'] = status.HTTP_400_BAD_REQUEST
            return data
        
        account = serialized_data.save()
        account.is_active = 0
        account.save()
        dependencies.register_for_new_user_service_instance.userRegister(email)

        data = {}
        data['message'] = "اطلاعات کاربر با موفقیت ثبت شد"
        data['status'] = status.HTTP_200_OK
        return data