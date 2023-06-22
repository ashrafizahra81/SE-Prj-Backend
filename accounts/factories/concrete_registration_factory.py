from .registration_factory import RegistrationFactory
from accounts.models import *
from rest_framework.views import APIView
from accounts.serializers import *
import logging
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger("django")
class UserRegistrationFactory(RegistrationFactory):

    def create_viewset(self):
        
        class UserRegisterViewset(APIView):

            def post(self, request):

                logger.info('request recieved from POST /accounts/register/')
                serialized_data = UserRegisterSerializer(data=request.data)

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

    def create_viewset(self):
        class ShopManagerRegisterViewset(APIView):
            def post(self, request):

                logger.info('request recieved from POST /accounts/create_shop/')
                serialized_data = ShopManagerRegisterSerializer(data=request.data)

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