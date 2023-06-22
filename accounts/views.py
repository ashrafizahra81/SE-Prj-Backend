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
from accounts.factories.concrete_registration_factory import *
from accounts.factories.concrete_edit_factory import *
from accounts.factories.concrete_show_info_factory import *

from django.http import HttpRequest

mail_service_instance = dependencies.mail_service_instance
uniqueCode_service_instance = dependencies.uniqueCode_service_instance
codeForUsers_service_instance = dependencies.codeForUsers_service_instance
register_for_existed_user_service_instance = dependencies.register_for_existed_user_service_instance
register_for_new_user_service_instance = dependencies.register_for_new_user_service_instance



logger = logging.getLogger("django")


class UserRegister(APIView):

    serializer_class = UserRegisterSerializer
    def post(self, request , type):
        if(type == 'customer'):
            user_registration_factory = UserRegistrationFactory()
        elif (type == 'shop'):
            user_registration_factory = ShopManagerRegistrationFactory()
        user_register_serializer = user_registration_factory.create_serializer()
        user_register_viewset = user_registration_factory.create_viewset()
        view = user_register_viewset.as_view()
        response = view(request = request._request)
        return response

class verfyUserToResgister(APIView):
    def post(self , request):
        logger.info('request recieved from POST /accounts/verify_email/')
        if(not(int(request.data['code']) <=999999 and int(request.data['code']) >= 100000)):
            logger.warn('The code entered is not in a right range')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if(CodesForUsers.objects.filter(code=int(request.data['code'])).exists()):
            logger.info('The code entered is valid')
            data = {}
            data = dependencies.verify_user_to_register_service_instance.verify_user_to_register(request.data['code'])
            return Response(data=data , status=status.HTTP_200_OK)
        
        logger.warn('code not found')
        return Response(status=status.HTTP_404_NOT_FOUND)

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer
    


class TokenVerifyView(TokenViewBase):
    
    serializer_class = CustomTokenVerifySerializer


class UserEditProfile(APIView):

    def post(self, request , type):
        if(type == 'customer'):
            edit_factory = ConcreteCustomerEditFactory()
        elif (type == 'shop'):
            edit_factory = ConcreteShopEditFactory()
        edit_viewset = edit_factory.create_viewset()
        view = edit_viewset.as_view()
        response = view(request = request._request)
        return response


class ShowUserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, type):

        if(type == 'customer'):
            show_info_factory = ConcreteUserShowInfoFactory()
        elif (type == 'shop'):
            show_info_factory = ConcreteShopShowInfoFactory()
        edit_viewset = show_info_factory.create_viewset()
        view = edit_viewset.as_view()
        response = view(request = request._request)
        return response



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

        dependencies.user_service_instance.updateUserPassword(used, password)

        logger.info('password of user '+str(used.pk)+' changed successfuly')
        return Response('Password changed successfully')
        
    logger.info('request recieved from GET /accounts/reset_password/')

    used=User.objects.get(id=request.user.id)
    token1 = mail_service_instance.propareEmailBody(used.email)
    dependencies.user_service_instance.updateUserCode(used,token1)
    # return dependencies.reset_password_info_service_instance.reset_password(request)

    dependencies.reset_password_info_service_instance.update_user_code(request.user.id)
    return Response({'message':'a token was sent to the user'}, status=status.HTTP_200_OK)


class ReceiveEmailForRecoverPassword(APIView):
    def post(self, request):
        
        token1 = dependencies.forget_password_info_service_instance.receiveEmailForRecoverPassword(request.data['email'])
        dependencies.user_service_instance.updateUserPassword(request.data['email'], str(token1))    

        # data3 = {}
        # data3['id'] = user.id
        
        return Response(status=status.HTTP_200_OK)

