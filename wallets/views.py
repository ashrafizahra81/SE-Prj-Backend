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
        data2 = request.data
        data = {}

        data = dependencies.charge_wallet_service_instance.check_money_in_wallet(data2['insert'])
        if data:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        dependencies.wallet_service_instance.updateWallet(request.user, data2['insert'])
        data = {}
        wallet = Wallet.objects.get(user=request.user)
        data['balance'] = wallet.balance
        logger.info('amount of '+str(request.data['insert'])+' added to wallet of user '+str(request.user.id))
        return Response(data, status=status.HTTP_200_OK)

