from django.shortcuts import render
from .models import *
from products.models import Product
from shoppingCarts.models import UserShoppingCart
from products.serializers import ProductsSerializer, EditProductSerializer, ProductsOfOrderSerializer
from accounts.models import User
from wallets.models import Wallet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from permissions import IsShopOwner
import logging
from Backend import settings
import importlib
from Backend import dependencies

logger = logging.getLogger("django")




class GetUserOrders(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logger.info('request recieved from GET /orders/user_orders/')
        user_orders = dependencies.userOrderService_instance.get_user_orders(request.user.id) 
        if user_orders:
            logger.info('Orders of user '+str(request.user.id)+' found successfuly')
            return Response(status=status.HTTP_200_OK, data=user_orders)
        else:
            logger.warn('No order found for user '+str(request.user.id))
            return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        logger.info('request recieved from POST /orders/checkout/')
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        price , off_price = dependencies.purchaseService_instance.calculate_price(user_cart)
        balance = dependencies.purchaseService_instance.check_type_of_payment(request.user.id , request.data['type'] , off_price)
        if(balance != None):
            if balance < 0:
                return Response({"message":"موجودی کیف پول شما برای این خرید کافی نیست"}, status=status.HTTP_204_NO_CONTENT)
        data = dependencies.purchaseService_instance.purchase(request.user, user_cart, price, off_price, balance)
        return Response(data, status=status.HTTP_200_OK)


class ShowOrdersToShop(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]
    def get(self, request):
        logger.info('request recieved from GET /orders/show_order_to_shop/')
        order_list = list(Order.objects.all().values())
        product_list = dependencies.show_order_to_shop_service_instance.show_orders_to_shop(order_list , request)
        if product_list:
            logger.info('orders from products of seller '+str(request.user.id)+' found')
            return Response(product_list, status=status.HTTP_200_OK)
        logger.warn('no order found from seller '+str(request.user.id))
        return Response(status=status.HTTP_204_NO_CONTENT)
