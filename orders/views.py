from django.shortcuts import render
from .models import *
from products.models import Product
from shoppingCarts.models import UserShoppingCart
from products.serializers import ProductsSerializer, EditProductSerializer
from accounts.models import User
from wallets.models import Wallet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from permissions import IsShopOwner
# Create your views here.


class GetUserOrders(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):

        user_orders = list(Order.objects.filter(user_id=request.user.id).values())
        data = list()
        for o in user_orders:
            print(o)
            product = Product.objects.get(pk=o['product_id'])
            serialized_product = ProductsSerializer(instance=product)
            js = serialized_product.data
            print('upload')
            js['cost'] = o['cost']
            # js['order_date'] = o['order_date']
            # js['complete_date'] = o['complete_date']
            js['status'] = o['status']
            data.append(js)
        if data:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        price = 0
        off_price = 0
        p_data = {}
        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            product_inventory = product1.inventory - 1
            product1.last_product_sold_date = datetime.today()
            if(product1.inventory==0):
                product1.is_available = 0
            p_data['inventory'] = product_inventory
            serialized_data = EditProductSerializer(instance=product1, data=p_data, partial=True)
            off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
            if serialized_data.is_valid():
                edited_product = serialized_data.save()
                
            price += product1.product_price

        wallet = Wallet.objects.get(user_id = request.user)
        if(request.data['type']=="wallet" and wallet.balance < off_price+30000):
            return Response({"message":"موجودی کیف پول شما برای این خرید کافی نیست"}, status=status.HTTP_204_NO_CONTENT)
        for o in user_cart:
            product = Product.objects.get(pk=o['product_id'])
            if product.is_deleted == False:
                c = Order(
                    user=request.user,
                    product=product,
                    cost=product.product_price,
                    total_cost=price+30000,
                    off_cost=off_price+30000,
                    status="Accepted",
                )
                c.save()
            UserShoppingCart.objects.filter(user_id=request.user.id).delete()
        user = User.objects.get(email=request.user)
        user.score += off_price / 100000 # each 100,000 Toman, 1 score
        user.save()
        if(request.data['type'] == "wallet"):
            wallet.balance = wallet.balance - (off_price+30000)
        data = {}
        data["message"] = "خرید با موفقیت انجام شد"
        data["balance"] = wallet.balance
        wallet.save()
        return Response(data, status=status.HTTP_200_OK)

class ShowOrdersToShop(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]

    def get(self, request):
        order_list = list(Order.objects.all().values())
        
        product_list = list()
        for order in order_list:
            # print(order)
            for product in Product.objects.all().values():
                self.check_object_permissions(request, product)
                print(product['id'])
                if product['id'] == order['product_id']:

                    if product['shop_id'] == request.user.id:
                        data = {}
                        data['id'] = product['id']
                        data['product_name'] = product['product_name']
                        data['product_size'] = product['product_size']
                        data['product_color'] = product['product_color']
                        data['product_price'] = product['product_price']
                        data['inventory'] = product['inventory']
                        data['upload'] = product['upload']
                        data['shop_id'] = product['shop_id']
                        product_list.append(data)
        if product_list:
            return Response(product_list, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
