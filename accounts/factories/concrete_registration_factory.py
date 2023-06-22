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

                    logger.info('This email already exists: ' + request.data['email'])
                    if (User.objects.get(email=request.data['email']).is_active == 1):
                        logger.info('This account is active: ' + request.data['email'])
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    if (dependencies.codeForUsers_service_instance.hasExpired(request.data['email'])):

                        dependencies.register_for_existed_user_service_instance.userRegister(
                            request.data['email'])
                        return Response({"message": "کد جدید به ایمیل ارسال شد"},
                                        status=status.HTTP_201_CREATED)

                    logger.info('User has valid code')
                    return Response({"message": "کد به ایمیل شما ارسال شده است"},
                                    status=status.HTTP_202_ACCEPTED)

                data = {}
                logger.info('no user with this email exists: '+request.data['email'])

                if serialized_data.is_valid():

                    return Response({"message":dependencies.save_new_user_info_service_instance.saveNewUser(serialized_data, request.data['email'], request.data['user_phone_number'])["message"]},
                                     status = dependencies.check_email_for_registration_info_service_instance.checkIfEmailExists(request.data['email'])["status"])

                    logger.info('Data entered is valid')
                    if (not (request.data['user_phone_number'].isdigit())):
                        logger.warn('user_phone_number is invalid')
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    account = serialized_data.save()
                    account.is_active = 0
                    account.save()
                    dependencies.register_for_new_user_service_instance.userRegister(
                        request.data['email'])
                    return Response(data=data, status=status.HTTP_200_OK)

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
            

                logger.info('request recieved from POST /accounts/create_shop/')
                serialized_data = ShopManagerRegisterSerializer(data=request.data)
                if(User.objects.filter(email=request.data['email']).exists()):
                    logger.info('This email already exists: ' + request.data['email'])
                    if(User.objects.get(email = request.data['email']).is_active == 1):
                        logger.info('This account is active: ' + request.data['email'])
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    
                    
                    if(dependencies.codeForUsers_service_instance.hasExpired(request.data['email'])):
                        
                        dependencies.register_for_existed_user_service_instance.userRegister(request.data['email'])
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
                    dependencies.register_for_new_user_service_instance.userRegister(request.data['email'])
                    return Response(data)
                logger.warn('could not save new user due to invalid data')
                return Response(serialized_data.errors ,status=status.HTTP_400_BAD_REQUEST)

        return ShopManagerRegisterViewset