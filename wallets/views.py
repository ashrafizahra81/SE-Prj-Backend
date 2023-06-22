from django.shortcuts import render
from .models import *
from shoppingCarts.models import UserShoppingCart
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from Backend import dependencies
import logging
logger = logging.getLogger("django")

class ChargeWallet(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self , request):
        logger.info('request recieved from POST /wallets/charge_wallet/')
        data = dependencies.charge_wallet_service_instance.check_money_in_wallet(request.data['insert'])
        if not data:
            balance = dependencies.wallet_service_instance.updateWallet(request.user, request.data['insert'])
            logger.info('amount of '+str(request.data['insert'])+' added to wallet of user '+str(request.user.id))
            return Response(balance, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

