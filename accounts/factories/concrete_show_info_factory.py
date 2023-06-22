from .show_info_factory import ShowInfoFactory
from accounts.models import *
from rest_framework.views import APIView
from accounts.serializers import *
import logging
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsShopOwner , IsShopManager

class ConcreteUserShowInfoFactory(ShowInfoFactory):

    def create_viewset(self):
        
        class UserShowInfoFactory(APIView):

            permission_classes = [IsAuthenticated, ]

            def get(self, request):
                logger.info('request recieved from GET /accounts/show_user_info/')
                userObj = User.objects.get(id=request.user.id)
                logger.info('user found')
                data = {}

                # data = dependencies.show_user_info_service_instance.show_user_info(request.user.id)
                user = ShowUserInfoSerializer(userObj)
                data = user.data

                return Response(data, status=status.HTTP_200_OK)
                    

                data = dependencies.show_user_info_service_instance.show_user_info(request.user.id)

                return Response(data, status=status.HTTP_200_OK)
        

        return UserShowInfoFactory





class ConcreteShopShowInfoFactory(ShowInfoFactory):
    def create_viewset(self):
        
        class ShopShowInfoFactory(APIView):

            permission_classes = [IsAuthenticated, ]

            def get(self, request):
                logger.info('request recieved from GET /accounts/show_user_info/')
                userObj = User.objects.get(id=request.user.id)
                logger.info('user found')
                data = {}
                
                shop = ShowShopManagerInfoSerializer(userObj)
                data = shop.data

                return Response(data, status=status.HTTP_200_OK)
        
        return ShopShowInfoFactory
    