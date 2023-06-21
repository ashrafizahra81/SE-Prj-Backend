from accounts.models import CodesForUsers
from .account_interface import CodeForUsersService, EditProfileService, MailService, RegisterService, CheckEmailForRegister, SaveNewUser, ResetPasswordService, ShowUserInfoService, UniqueCodeService, UserService, VerfyUserToResgisterService
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import importlib
from .mail_interface import MailService
from Backend import dependencies
from ..models import User
from wallets.models import Wallet
import random
from django.contrib.auth.hashers import make_password
from accounts.serializers import *


import logging

logger = logging.getLogger("django")

username='ashzar638@gmail.com'
password='cstlshkgpoiwbhlj'

# mail_service_instance = dependencies.mail_service_instance
codeForUsers_service_instance = dependencies.codeForUsers_service_instance
user_service_instance = dependencies.user_service_instance
wallet_service_instance = dependencies.wallet_service_instance


class ConcreteCodeForUsersService(CodeForUsersService):

    def checkIfTheCodeExists(self, token):
        return CodesForUsers.objects.filter(code=token).exists()

    def createCodesForUsers(self, token, email, date):
        user_code = CodesForUsers(
            code = token,
            created_at = date,
            email = email 
        )
        user_code.save()
    
    def updateCodesForUsers(self, token, email, date):
        userCode = CodesForUsers.objects.get(email = email)
        userCode.created_at = date
        userCode.code = token
        userCode.save()

    def hasExpired(self, email):
        userCode = CodesForUsers.objects.get(email = email)
        now = datetime.now()
        delta = now - userCode.created_at.replace(tzinfo=None)
        diff = delta.seconds

        return diff > 600
class ConcreteEditProfileService(EditProfileService):

    def edit_profile(slf, serialized_data):
        
        if(not(serialized_data.data['user_postal_code'].isdigit())):
            logger.warn('The user postal code entered is invalid')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(not(serialized_data.data['user_phone_number'].isdigit())):
            logger.warn('The user phone number entered is invalid')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logger.info('Data entered is valid')
        edited_user = serialized_data.save()

        return Response(serialized_data.data, status=status.HTTP_200_OK)

class ConcreteMailService(MailService):

    def send_mail(self, html, text, subject, from_email, to_emails):
        assert isinstance(to_emails,list)
        msg=MIMEMultipart('alternative')
        msg['From']=username
        msg['To']=", ".join(to_emails)
        msg['Subject']=subject
        txt_part=MIMEText(text,'plain')
        msg.attach(txt_part)


        html_part = MIMEText(f"<p>Here is your password reset token</p><h1>{html}</h1>", 'html')
        msg.attach(html_part)
        msg_str=msg.as_string()



        server=smtplib.SMTP(host='smtp.gmail.com',port=587)
        server.ehlo()
        server.starttls()

        server.login(username,password)
        server.sendmail(from_email,to_emails,msg_str)
        server.quit()

 
    def sendEmail(self, email):
    
        uniqueCode_service_instance = dependencies.uniqueCode_service_class
        
        token = uniqueCode_service_instance.getUniqueCode(self)
        to_emails = []
        to_emails.append(email)
        self.send_mail(html=token,text='Here is the code ',subject='verification',from_email='',to_emails=to_emails)
        logger.info('The verification code has been sent to the email')
        return token

class ConcreteUserRegisterServiceForExistedUser(RegisterService):

    def userRegister(self, email):


        
        logger.info('This email already exists: ' +email)

        userCode = CodesForUsers.objects.get(email = email)
        now = datetime.now()
        delta = now - userCode.created_at.replace(tzinfo=None)
        diff = delta.seconds
        token = dependencies.mail_service_instance.sendEmail(userCode.email)
        dependencies.codeForUsers_service_instance.updateCodesForUsers(token, email, datetime.now())
        logger.info('The code stored in database for user '+userCode.email)
    
class ConcreteUserRegisterServiceForNewUser(RegisterService):

    def userRegister(self, email):

        # user_service_instance.updateUser(serialized_data, 0)
        
        token = dependencies.mail_service_instance.sendEmail(email)
        dependencies.codeForUsers_service_instance.createCodesForUsers(token, email, datetime.now())

        account = User.objects.get(email = email)
        wallet_service_instance.createWallet(account, 0)

        logger.info('User ' + str(account.pk)+ ' and its code stored in database')
    

class ConcreteCheckEmailForRegister(CheckEmailForRegister):

    def checkIfEmailExists(self, email):
        
        logger.info('This email already exists: ' + email)
        if(User.objects.get(email = email).is_active == 1):
            logger.info('This account is active: ' + email)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if(dependencies.codeForUsers_service_instance.hasExpired(email)):
            
            
            dependencies.register_for_existed_user_service_instance.userRegister(email)
            return Response({"message":"کد جدید به ایمیل ارسال شد"},
                    status=status.HTTP_201_CREATED)
            

        logger.info('User has valid code')
        return Response({"message":"کد به ایمیل شما ارسال شده است"},
                        status=status.HTTP_202_ACCEPTED)

class ConcreteSaveNewUserService(SaveNewUser):
    
    def saveNewUser(self, serialized_data, email, phone_number):
        logger.info('Data entered is valid')
        if(not(phone_number.isdigit())):
            logger.warn('user_phone_number is invalid')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        account = serialized_data.save()
        account.is_active = 0
        account.save()
        dependencies.register_for_new_user_service_instance.userRegister(email)
        return Response(data = {} , status=status.HTTP_200_OK)

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
class ConcreteUniqueCodeService(UniqueCodeService):

    def getUniqueCode(self):
        # codeForUsers_service_instance = dependencies.codeForUsers_service_instance
        while(True):
            token = random.randint(100000,999999)
            if(not(dependencies.codeForUsers_service_instance.checkIfTheCodeExists(token))):
                return token
    
class ConcreteUserService(UserService):
    def updateUser(self, data, is_valid):
        
        serialized_data = UserRegisterSerializer(data=data)
        if serialized_data.is_valid():
            account = serialized_data.save()
            account.is_active = is_valid
            account.save()

    def updateUserScore(self, score, email):
        user = User.objects.get(email=email)
        user.score += score
        user.save() 

    def updateUserIsValid(self, user, is_valid):
        user.is_active = is_valid
        user.save()
    
    def updateUserPassword(self, user, password):

        user.random_integer=None
        user.password = make_password(password)
        user.save()
    
    def updateUserCode(self, user, code):
        user.random_integer=code
        user.save()
        
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