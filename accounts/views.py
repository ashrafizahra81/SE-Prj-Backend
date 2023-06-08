from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .serializers import *
from .models import *
from rest_framework import status
from datetime import datetime
import random
from wallets.models import Wallet
from rest_framework.decorators import api_view, permission_classes
from . import send_mail
from django.contrib.auth.hashers import make_password
from datetime import datetime
from permissions import IsShopOwner , IsShopManager
import logging
from Backend import dependencies

mail_service_instance = dependencies.mail_service_instance
uniqueCode_service_instance = dependencies.uniqueCode_service_instance
codeForUsers_service_instance = dependencies.codeForUsers_service_instance
register_for_existed_user_service_instance = dependencies.register_for_existed_user_service_instance
register_for_new_user_service_instance = dependencies.register_for_new_user_service_instance


logger = logging.getLogger("django")


class UserRegister(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):

        logger.info('request recieved from POST /accounts/register/')
        serialized_data = UserRegisterSerializer(data=request.data)
        if(User.objects.filter(email=request.data['email']).exists()):
            logger.info('This email already exists: ' + request.data['email'])
            if(User.objects.get(email = request.data['email']).is_active == 1):
                logger.info('This account is active: ' + request.data['email'])
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            if(codeForUsers_service_instance.hasExpired(request.data['email'])):
                register_for_existed_user_service_instance.userRegister(serialized_data)
                return Response({"message":"کد جدید به ایمیل ارسال شد"},
                            status=status.HTTP_201_CREATED)

            logger.info('User has valid code')
            return Response({"message":"کد به ایمیل شما ارسال شده است"},
                            status=status.HTTP_202_ACCEPTED)
        data = {}
        logger.info('no user with this email exists: '+request.data['email'])
        if serialized_data.is_valid():
            logger.info('Data entered is valid')
            if(not(request.data['user_phone_number'].isdigit())):
                logger.warn('user_phone_number is invalid')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            register_for_new_user_service_instance.userRegister(serialized_data)
            return Response(data = data , status=status.HTTP_200_OK)
        
        logger.warn('could not save new user due to invalid data')
        return Response(serialized_data.errors , status=status.HTTP_400_BAD_REQUEST)

class verfyUserToResgister(APIView):
    def post(self , request):
        logger.info('request recieved from POST /accounts/verify_email/')
        if(not(int(request.data['code']) <=999999 and int(request.data['code']) >= 100000)):
            logger.warn('The code entered is not in a right range')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(CodesForUsers.objects.filter(code=int(request.data['code'])).exists()):
            logger.info('The code entered is valid')
            userCode = CodesForUsers.objects.get(code = int(request.data['code']))
            logger.info('code for user with email '+ userCode.email+' deleted')
            user = User.objects.get(email = userCode.email)
            CodesForUsers.objects.filter(code=int(request.data['code'])).delete()
            user.is_active = 1
            user.save()
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
            return Response(data=data , status=status.HTTP_200_OK)
        logger.warn('code not found')
        return Response(status=status.HTTP_404_NOT_FOUND)

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    


class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    
    serializer_class = CustomTokenVerifySerializer


class UserEditProfile(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserEditProfileSerializer
    def post(self, request):
        logger.info('request recieved from POST /accounts/edit_profile/')
        user = User.objects.get(id=request.user.id)
        logger.info('user found')
        data1 = {}

        data1['email'] = user.email
        data1['username'] = user.username
        data1['user_phone_number'] = user.user_phone_number
        data1['user_postal_code'] = user.user_postal_code
        data1['user_address'] = user.user_address

        data = {}

        serialized_data = UserEditProfileSerializer(instance=user, data=request.data, partial=True)
        if serialized_data.is_valid():
            if(not(request.data['user_postal_code'].isdigit())):
                logger.warn('The user postal code entered is invalid')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if(not(request.data['user_phone_number'].isdigit())):
                logger.warn('The user phone number entered is invalid')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            logger.info('Data entered is valid')
            edited_user = serialized_data.save()
            if data1['email'] != edited_user.email:
                data['email'] = edited_user.email
                logger.info('Email changed from '+data1['email']+' to '+ edited_user.email)
            else:
                data['email'] = ""

            if data1['username'] != edited_user.username:
                data['username'] = edited_user.username
                logger.info('username changed from '+data1['username']+' to '+ edited_user.username)

            else:
                data['username'] = ""
            if data1['user_phone_number'] != edited_user.user_phone_number:
                data['user_phone_number'] = edited_user.user_phone_number
                logger.info('user_phone_number changed from '+data1['user_phone_number']+' to '+ edited_user.user_phone_number)

            else:
                data['user_phone_number'] = ""

            if data1['user_postal_code'] != edited_user.user_postal_code:
                data['user_postal_code'] = edited_user.user_postal_code
                logger.info('user_postal_code changed from '+str(data1['user_postal_code'])+' to '+ str(edited_user.user_postal_code))

            else:
                data['user_postal_code'] = ""

            if data1['user_address'] != edited_user.user_address:
                data['user_address'] = edited_user.user_address
                logger.info('user_address changed from '+str(data1['user_address'])+' to '+ str(edited_user.user_address))

            else:
                data['user_address'] = ""

            return Response(serialized_data.data, status=status.HTTP_200_OK)
        
        logger.warn('The data entered is invalid')
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopManagerRegister(APIView):
    serializer_class = ShopManagerRegisterSerializer
    def post(self, request):
        logger.info('request recieved from POST /accounts/create_shop/')
        serialized_data = ShopManagerRegisterSerializer(data=request.data)
        if(User.objects.filter(email=request.data['email']).exists()):
            logger.info('This email already exists: ' + request.data['email'])
            if(User.objects.get(email = request.data['email']).is_active == 1):
                logger.info('This account is active: ' + request.data['email'])
                return Response(status=status.HTTP_400_BAD_REQUEST)
            userCode = CodesForUsers.objects.get(email = request.data['email'])
            now = datetime.now()
            delta = now - userCode.created_at.replace(tzinfo=None)
            diff = delta.seconds
            if(diff > 600):
                token = sendEmail(self , userCode.email)
                userCode.created_at = datetime.now()
                userCode.code = token
                userCode.save()
                logger.info('New verification code has been sent')
                return Response({"message":"کد جدید به ایمیل ارسال شد"},
                            status=status.HTTP_201_CREATED)
            logger.info('User has valid code')
            return Response({"message":"کد به ایمیل شما ارسال شده است"},
                            status=status.HTTP_202_ACCEPTED)
        data = {}
        logger.info('no user with this email exists: '+request.data['email'])
        if serialized_data.is_valid():
            logger.info('Data entered is valid')
            if(not(request.data['shop_phone_number'].isdigit())):
                logger.warn('shop_phone_number is invalid')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            account = serialized_data.save()
            account.is_active = 0
            account.save()
            token = sendEmail(self , account.email)
            user_code = CodesForUsers(
                code = token,
                created_at = datetime.now(),
                email = account.email 
            )
            user_code.save()
            logger.info('User '+str(account.pk)+ ' saved successfully')
            return Response(data)
        logger.warn('could not save new user due to invalid data')
        return Response(serialized_data.errors ,status=status.HTTP_400_BAD_REQUEST)


class EditShop(APIView):
    permission_classes = [IsAuthenticated ,IsShopManager]
    serializer_class = EditShopSerializer
    def post(self, request):
        logger.info('request recieved from POST /accounts/edit_shop/')
        self.check_object_permissions(request, request.user)
        logger.info('The user is a shop owner')
        user = User.objects.get(id=request.user.id)
        data1 = {}
        data1['username'] = user.username
        data1['user_phone_number'] = user.user_phone_number
        data1['email'] = user.email
        data1['shop_address'] = user.shop_address
        data1['shop_name'] = user.shop_name
        data1['shop_phone_number'] = user.shop_phone_number
        serialized_data = EditShopSerializer(data=request.data, instance=user, partial=True)
        data = {}
        if serialized_data.is_valid():
            if(not(request.data['shop_phone_number'].isdigit())):
                logger.warn('The shop phone number entered is invalid')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if(not(request.data['user_phone_number'].isdigit())):
                logger.warn('The user phone number entered is invalid')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            logger.info('Data entered is valid')
            edited_shop = serialized_data.save()

            if data1['username'] != edited_shop.username:
                data['username'] = edited_shop.username
                logger.info('username changed from '+data1['username']+' to '+ edited_shop.username)
            else:
                data['username'] = ""

            if data1['user_phone_number'] != edited_shop.user_phone_number:
                data['user_phone_number'] = edited_shop.user_phone_number
                logger.info('user_phone_number changed from '+str(data1['user_phone_number'])+' to '+ str(edited_shop.user_phone_number))
            else:
                data['user_phone_number'] = ""

            if data1['email'] != edited_shop.email:
                data['email'] = edited_shop.email
                logger.info('Email changed from '+data1['email']+' to '+ edited_shop.email)
            else:
                data['email'] = ""

            if data1['shop_address'] != edited_shop.shop_address:
                data['shop_address'] = edited_shop.shop_address
                logger.info('shop_address changed from '+data1['shop_address']+' to '+ edited_shop.shop_address)
            else:
                data['shop_address'] = ""

            if data1['shop_name'] != edited_shop.shop_name:
                data['shop_name'] = edited_shop.shop_name
                logger.info('shop_name changed from '+data1['shop_name']+' to '+ edited_shop.shop_name)

            else:
                data['shop_name'] = ""

            if data1['shop_phone_number'] != edited_shop.shop_phone_number:
                data['shop_phone_number'] = edited_shop.shop_phone_number
                logger.info('shop_phone_number changed from '+data1['shop_phone_number']+' to '+ edited_shop.shop_phone_number)

            else:
                data['shop_phone_number'] = ""

            return Response(serialized_data.data, status=status.HTTP_200_OK)
        logger.warn('The data entered is invalid')
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
      

class ShowUserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logger.info('request recieved from GET /accounts/show_user_info/')
        userObj = User.objects.get(id=request.user.id)
        logger.info('user found')
        data = {}
        if userObj.shop_name == None:
            logger.info('user '+str(userObj.pk)+ ' is a customer')
            data['email'] = userObj.email
            data['username'] = userObj.username
            data['user_phone_number'] = userObj.user_phone_number
            data['user_postal_code'] = userObj.user_postal_code
            data['user_address'] = userObj.user_address
            wallet = Wallet.objects.get(user = userObj)
            data['inventory'] = wallet.balance
        else:
            logger.info('user '+str(userObj.pk)+ ' is a seller')
            data['email'] = userObj.email
            data['username'] = userObj.username
            data['shop_name'] = userObj.shop_name
            data['shop_phone_number'] = userObj.shop_phone_number
            data['user_phone_number'] = userObj.user_phone_number
            data['shop_address'] = userObj.shop_address

        return Response(data, status=status.HTTP_200_OK)


class show_score(APIView):
     permission_classes = [IsAuthenticated, ]
     def get(self , request):
        logger.info('request recieved from GET /accounts/show_score/')
        data = {}
        data['score'] = request.user.score
        logger.info('score of user '+str(request.user.pk)+' is '+str(request.user.score))
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reset_password(request):
    if request.method =='POST':
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
        used.random_integer=None
        used.password = make_password(password)
        used.save()
        logger.info('password of user '+str(used.pk)+' changed successfuly')
        return Response('Password changed successfully')
    logger.info('request recieved from GET /accounts/reset_password/')
    token1=random.randint(1000,9999)
    used=User.objects.get(id=request.user.id)
    used.random_integer=token1
    used.save()
    to_emails = []
    to_emails.append(used.email)
    send_mail.send_mail(html=token1,text='Here is your password reset token',subject='password reset token',from_email='',to_emails=to_emails)
    return Response({'message':'a token was sent to the user'}, status=status.HTTP_200_OK)



class ReceiveEmailForRecoverPassword(APIView):
    def post(self, request):
        logger.info('request recieved from POST /accounts/receive_email_for_recover_password/')
        data = request.data
        email1 = data['email']
        # user = CodesForUsers.objects.filter(email=email1).exists()
        # if user != False:
        #     logger.info('user with email '+email1+' has a code')
        #     user = CodesForUsers.objects.get(email=email1)
        #     now = datetime.now()
        #     delta = now - user.created_at.replace(tzinfo=None)
        #     diff = delta.seconds
        #     if diff > 600:
        #         logger.info('The code of user with email '+email1+' has expired')
        #         token1=getUniqueCode()
        #         user.code = token1
        #         user.created_at = datetime.now()
        #         user.save()
        #         logger.info('a new code assigned user with email '+email1)
        # else:
        #     logger.info('user with email '+email1+'does not have a code')
        #     token1=getUniqueCode()
        #     user = CodesForUsers(
        #         code = token1,
        #         created_at = datetime.now(),
        #         email= email1,
        #     )
        #     user.save()
        #     logger.info('a new code assigned user with email '+email1)
        user = User.objects.get(email=email1)
        token1=getUniqueCode()
        user.password = make_password(str(token1))
        user.save()
        to_emails = []
        to_emails.append(user.email)
        send_mail.send_mail(html=token1,text='Here is your new password',subject='password recovery token',from_email='',to_emails=to_emails)
        data3 = {}
        data3['id'] = user.id
        

        return Response(data3, status=status.HTTP_200_OK)

# class RecoverPassword(APIView):
#     def post(self, request, pk):
#         data2 = request.data
#         token_recieved=data2['token']
#         password=data2['password']
#         password_again=data2['password2']
#         user = CodesForUsers.objects.get(pk=pk)
#         data3 = {}
#         data3['code-id'] = user.id
#         if token_recieved !=user.code:
#             logger.warn('token entered '+token_recieved+' is not equal with '+user.code)
#             return Response({'message':'Invalid Token'} , status=status.HTTP_400_BAD_REQUEST)
#         if password!=password_again:
#             logger.warn('password_again '+password_again+' is not equal with password'+password)
#             return Response({'message':'Passwords should match'} , status=status.HTTP_400_BAD_REQUEST)
#         mainUser = User.objects.get(email=user.email)
#         mainUser.password = make_password(password)
#         mainUser.save()
#         logger.info('password of user with email '+mainUser.email+' changed successfuly')
#         return Response({'message':'Password changed successfully'} , status=status.HTTP_200_OK)