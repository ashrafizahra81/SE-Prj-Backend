from django.shortcuts import render
from .models import *
from accounts.models import User
from shoppingCarts.models import UserShoppingCart
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
# Create your views here.


class ShowGiftInfo(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self , request):
        data = []
        for i in Gift.objects.all().values():
            if(datetime(i["date"].year, i["date"].month, i["date"].day) >= datetime.now()):
                data1={}
                data1['description'] = i['description']
                data1['score'] = i['score']
                data1['date'] = i['date']
                data.append(data1)
        if(len(data) == 0):
            return Response({"message":"درحال حاضر جایزه‌ای فعال نیست"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data, status=status.HTTP_200_OK)

class getGift(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self,request):
        user = User.objects.get(email=request.user)
        gift = Gift.objects.get(score = request.data['score'])
        if(user.score >= gift.score):
            user.gift = gift
            user.score = user.score - gift.score
            user.save()
            data = {}
            data['discount_code'] = gift.discount_code
            data['new_score'] = user.score
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message":"امتیاز شما کافی نیست"},status=status.HTTP_204_NO_CONTENT)

class applyDiscount(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self , request):
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        off_price = 0
        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
        data={}
        gift = Gift.objects.get(discount_code = request.data['discount_code'])
        if(datetime(gift.date.year, gift.date.month, gift.date.day) < datetime.now()):
            return Response({"message":"زمان استفاده از این کد تخفیف به انمام رسیده است"}
                        ,status=status.HTTP_204_NO_CONTENT)
        if(gift.type=='C'):
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = off_price
        if(gift.type == 'A'):
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = (0.8) * (off_price+30000)
        else:
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = (0.7) * (off_price+30000)
        data['shippingPrice'] = 30000
        return Response(data,status=status.HTTP_200_OK)