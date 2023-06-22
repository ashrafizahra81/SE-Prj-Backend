from .edit_factory import EditFactory
from accounts.models import *
from rest_framework.views import APIView
from accounts.serializers import *
import logging
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsShopOwner , IsShopManager



class ConcreteCustomerEditFactory(EditFactory):

    def create_viewset(self):

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
                    if(not(request.data['user_postal_code'].isdigit())):
                        logger.warn('The user postal code entered is invalid')
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    if(not(request.data['user_phone_number'].isdigit())):
                        logger.warn('The user phone number entered is invalid')
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    logger.info('Data entered is valid')
                    edited_user = serialized_data.save()

                    return Response(serialized_data.data, status=status.HTTP_200_OK)
                
                logger.warn('The data entered is invalid')
                return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return UserEditProfile

class ConcreteShopEditFactory(EditFactory):

    def create_viewset(self):
        
        class ShopEditProfile(APIView):


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
                    if(not(request.data['shop_phone_number'].isdigit())):
                        logger.warn('The shop phone number entered is invalid')
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    if(not(request.data['user_phone_number'].isdigit())):
                        logger.warn('The user phone number entered is invalid')
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    
                    logger.info('Data entered is valid')
                    edited_shop = serialized_data.save()

                    return Response(serialized_data.data, status=status.HTTP_200_OK)
                logger.warn('The data entered is invalid')
                return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return ShopEditProfile