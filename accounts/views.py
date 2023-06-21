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

            return Response({"message": dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["message"]}, status = dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["status"])
            # return dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])

        logger.info('no user with this email exists: '+request.data['email'])

        if serialized_data.is_valid():
            return dependencies.save_new_user_info_service_instance.saveNewUser(serialized_data, request.data['email'], request.data['user_phone_number'])
        
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
            data = {}
            data = dependencies.verify_user_to_register_service_instance.verify_user_to_register(request.data['code'])
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

        data = {}

        serialized_data = UserEditProfileSerializer(instance=user, data=request.data, partial=True)
        if serialized_data.is_valid():
            # if(not(request.data['user_postal_code'].isdigit())):
            #     logger.warn('The user postal code entered is invalid')
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            # if(not(request.data['user_phone_number'].isdigit())):
            #     logger.warn('The user phone number entered is invalid')
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            # logger.info('Data entered is valid')
            # edited_user = serialized_data.save()

            # return Response(serialized_data.data, status=status.HTTP_200_OK)
            return dependencies.edit_profile_info_service_instance.edit_profile(serialized_data)
        
        logger.warn('The data entered is invalid')
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopManagerRegister(APIView):
    serializer_class = ShopManagerRegisterSerializer
    def post(self, request):
        logger.info('request recieved from POST /accounts/create_shop/')
        serialized_data = ShopManagerRegisterSerializer(data=request.data)

        if(User.objects.filter(email=request.data['email']).exists()):
           
           return dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])

        logger.info('no user with this email exists: '+request.data['email'])
        if serialized_data.is_valid():
            return dependencies.save_new_user_info_service_instance.saveNewUser(serialized_data, request.data['email'], request.data['shop_phone_number'])\
        
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

        serialized_data = EditShopSerializer(data=request.data, instance=user, partial=True)
        data = {}
        if serialized_data.is_valid():
            # if(not(request.data['shop_phone_number'].isdigit())):
            #     logger.warn('The shop phone number entered is invalid')
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            # if(not(request.data['user_phone_number'].isdigit())):
            #     logger.warn('The user phone number entered is invalid')
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            
            # logger.info('Data entered is valid')
            # edited_shop = serialized_data.save()

            # return Response(serialized_data.data, status=status.HTTP_200_OK)
            return dependencies.edit_profile_info_service_instance.edit_profile(serialized_data)
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
            data = dependencies.show_user_info_service_instance.show_user_info(request.user.id)
        else:
            # data = dependencies.show_shop_manager_info_service_instance.show_user_info(request.user.id)

            shop = ShowShopManagerInfoSerializer(userObj)
            data = shop.data


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
        # logger.info('request recieved from POST /accounts/reset_password/')
        # data2 = request.data
        # token_recieved=data2['token']
        # password=data2['password']
        # password_again=data2['password2']
        # used = User.objects.get(id=request.user.id)
        # if int(token_recieved) !=used.random_integer:
        #     logger.warn('token entered '+str(token_recieved)+' is not equal with '+str(used.random_integer))
        #     return Response({'message':'Invalid Token'} , status=status.HTTP_400_BAD_REQUEST)

        # if password!=password_again:
        #     logger.warn('password_again '+password_again+' is not equal with password'+password)
        #     return Response({'message':'Passwords should match'} , status=status.HTTP_400_BAD_REQUEST)

        # dependencies.user_service_instance.updateUserPassword(used, password)

        # logger.info('password of user '+str(used.pk)+' changed successfuly')
        # return Response('Password changed successfully')
        return dependencies.reset_password_info_service_instance.reset_password(request)
    # logger.info('request recieved from GET /accounts/reset_password/')

    # used=User.objects.get(id=request.user.id)
    # token1 = mail_service_instance.sendEmail(used.email)
    # dependencies.user_service_instance.updateUserCode(used,token1)

    dependencies.reset_password_info_service_instance.update_user_code(request.user.id)
    return Response({'message':'a token was sent to the user'}, status=status.HTTP_200_OK)



class ReceiveEmailForRecoverPassword(APIView):
    def post(self, request):
        
        token1 = dependencies.forget_password_info_service_instance.receiveEmailForRecoverPassword(request.data['email'])
        dependencies.user_service_instance.updateUserPassword(request.data['email'], str(token1))    

        # data3 = {}
        # data3['id'] = user.id
        
        return Response(status=status.HTTP_200_OK)


















from rest_framework.views import APIView

# Abstract Factory
class RegistrationFactory:
    def create_serializer(self):
        pass

    def create_viewset(self):
        pass
# Concrete Factory for User Registration
class UserRegistrationFactory(RegistrationFactory):
    def create_serializer(self):
        class UserRegisterSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = '__all__'
        return UserRegisterSerializer
    def create_viewset(self):
        class UserRegisterViewset(APIView):
            serializer_class = self.create_serializer()
            def post(self, request):
                pass
        return UserRegisterViewset
# Concrete Factory for Shop Manager Registration
class ShopManagerRegistrationFactory(RegistrationFactory):
    def create_serializer(self):
        class ShopManagerRegisterSerializer(serializers.ModelSerializer):
            class Meta:
                model = ShopManager
                fields = '__all__'
        return ShopManagerRegisterSerializer

    def create_viewset(self):
        class ShopManagerRegisterViewset(APIView):
            serializer_class = self.create_serializer()

            def post(self, request):
                
                pass
        return ShopManagerRegisterViewset






# Create an instance of User Registration Factory
user_registration_factory = UserRegistrationFactory()
user_register_serializer = user_registration_factory.create_serializer()
user_register_viewset = user_registration_factory.create_viewset()

# Create an instance of Shop Manager Registration Factory
shop_manager_registration_factory = ShopManagerRegistrationFactory()
shop_manager_register_serializer = shop_manager_registration_factory.create_serializer()
shop_manager_register_viewset = shop_manager_registration_factory.create_viewset()
