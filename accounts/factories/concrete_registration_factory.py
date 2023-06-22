from .registration_factory import RegistrationFactory
from accounts.models import *
from rest_framework.views import APIView
# from accounts.serializers import *
from rest_framework import serializers
import logging
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger("django")
class UserRegistrationFactory(RegistrationFactory):

    def create_serializer(self):

        class UserRegisterSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ('username', 'email', 'user_phone_number', 'password')
                extera_kwargs = {
                    'password': {'write_only': True}
                }
        
        return UserRegisterSerializer

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        

    def create_viewset(self):

        class UserRegisterViewset(APIView):

            def post(self, request):

                logger.info('request recieved from POST /accounts/register/')
                register_serializer = UserRegistrationFactory.create_serializer(self)
                serialized_data = register_serializer(data=request.data)

                if (User.objects.filter(email=request.data['email']).exists()):


                    return Response({"message": dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["message"]},
                                     status = dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["status"])


                data = {}
                logger.info('no user with this email exists: '+request.data['email'])

                if serialized_data.is_valid():


                    return Response({"message":dependencies.save_new_user_info_service_instance.saveNewUser(serialized_data, request.data['email'], request.data['user_phone_number'])["message"]},
                                     status = dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["status"])

                logger.warn('could not save new user due to invalid data')
                return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return UserRegisterViewset
    


class ShopManagerRegistrationFactory(RegistrationFactory):

    def create_serializer(self):

        class ShopManagerRegisterSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ('username', 'email', 'password', 'shop_name', 'shop_address',
                        'shop_phone_number')
                extera_kwargs = {
                    'password': {'write_only': True}
                }
        return ShopManagerRegisterSerializer

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def create_viewset(self):
        class ShopManagerRegisterViewset(APIView):
            def post(self, request):


                logger.info('request recieved from POST /accounts/create_shop/')
                register_serializer = ShopManagerRegistrationFactory.create_serializer(self)
                serialized_data = register_serializer(data=request.data)

                if(User.objects.filter(email=request.data['email']).exists()):

                    return Response({"message": dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["message"]},
                                     status = dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["status"])
                data = {}
                logger.info('no user with this email exists: '+request.data['email'])

                if serialized_data.is_valid():
                    return Response({"message":dependencies.save_new_user_info_service_instance.saveNewUser(serialized_data, request.data['email'], request.data['user_phone_number'])["message"]},
                                     status = dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["status"])
                
                logger.warn('could not save new user due to invalid data')
                return Response(serialized_data.errors ,status=status.HTTP_400_BAD_REQUEST)
            

        return ShopManagerRegisterViewset