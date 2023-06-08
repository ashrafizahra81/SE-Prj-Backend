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
        price = 0
        off_price = 0
        for o1 in user_cart:
            product = Product.objects.get(pk=o1['product_id'])
            dependencies.purchaseService_instance.decrease_number_of_product(product)
            off_price += ((100 - product.product_off_percent) / 100) * product.product_price
            price += product.product_price
        
        wallet = Wallet.objects.get(user_id = request.user)
        balance = wallet.balance
        if(request.data['type']=="wallet"):
            logger.info('balance of wallet is '+str(wallet.balance))
            balance = dependencies.purchaseService_instance.buy_from_wallet(wallet , off_price+30000)
            if balance != None:
                logger.info('balance of wallet reduced to '+str(balance))
            else:
                logger.warn('wallet balance of user '+str(request.user.id)+ ' is not enough')
                return Response({"message":"موجودی کیف پول شما برای این خرید کافی نیست"}, status=status.HTTP_204_NO_CONTENT)
        for o in user_cart:
            product = Product.objects.get(pk=o['product_id'])
            if product.is_deleted == False:
                dependencies.cerate_order_service_instance(request.user , product, product.product_price ,price+30000 ,off_price+30000,"Accepted")
            UserShoppingCart.objects.filter(user_id=request.user.id).delete()
        logger.info('order of user '+str(request.user.id)+' saved successfuly')
        dependencies.user_service_instance.updateUserScore(off_price / 100000 , request.user)
        logger.info('score of this shop added to scores of user ' +str(request.user.id))            
        data = {}
        data["message"] = "خرید با موفقیت انجام شد"
        data["balance"] = balance
        return Response(data, status=status.HTTP_200_OK)

class ShowOrdersToShop(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]

    def get(self, request):
        logger.info('request recieved from GET /orders/show_order_to_shop/')
        order_list = list(Order.objects.all().values())
        product_list = list()
        for order in order_list:
            for product in Product.objects.all().values():
                self.check_object_permissions(request, product)
                if product['id'] == order['product_id']:
                    if product['shop_id'] == request.user.id:
                        data = ProductsOfOrderSerializer(product)
                        product_list.append(data.data)
        if product_list:
            logger.info('orders from products of seller '+str(request.user.id)+' found')
            return Response(product_list, status=status.HTTP_200_OK)
        logger.warn('no order found from seller '+str(request.user.id))
        return Response(status=status.HTTP_204_NO_CONTENT)
