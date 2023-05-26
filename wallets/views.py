from django.shortcuts import render
from .models import *
from shoppingCarts.models import UserShoppingCart
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import logging
logger = logging.getLogger("django")

class ChargeWallet(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self , request):
        logger.info('request recieved from POST /wallets/charge_wallet/')
        wallet = Wallet.objects.get(user=request.user)
        data2 = request.data
        data = {}
        if(data2['insert'] == '' or data2['insert'] < 0 or data2['insert'] == 0):
            logger.warn('data entered is invalid')
            data={"message": "مقدار وارد شده قابل قبول نیست"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        wallet.balance += float(data2['insert'])
        wallet.save()
        data['balance'] = wallet.balance
        logger.info('amount of '+str(request.data['insert'])+' added to wallet of user '+str(request.user.id))
        return Response(data, status=status.HTTP_200_OK)

