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
import logging
logger = logging.getLogger("django")

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
                logger.info('gift with id ' +str(i['id'])+' found')
        if(len(data) == 0):
            logger.warn('No gift is available')
            return Response({"message":"درحال حاضر جایزه‌ای فعال نیست"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data, status=status.HTTP_200_OK)

class GetGift(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self,request):
        if(type(request.data['score'])== str):
            if(not(request.data['score'].isdigit())):
                logger.warn('format of score entered is not correct')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=request.user)
        gift = Gift.objects.get(score = request.data['score'])
        if(user.score >= gift.score):
            user.gift = gift
            user.score = user.score - gift.score
            user.save()
            data = {}
            data['discount_code'] = gift.discount_code
            data['new_score'] = user.score
            logger.info('The gifts with id '+str(gift.id) +' assigned to the user with id '+str(user.id))
            return Response(data, status=status.HTTP_200_OK)
        logger.warn('the score of user '+str(user.id)+' is not enough for gift '+str(gift.id))
        return Response({"message":"امتیاز شما کافی نیست"},status=status.HTTP_204_NO_CONTENT)

class ApplyDiscount(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self , request):
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        off_price = 0
        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
        logger.info('total price of shopping cart calculated: '+str(off_price))
        data={}
        gift = Gift.objects.get(discount_code = request.data['discount_code'])
        if(datetime(gift.date.year, gift.date.month, gift.date.day) < datetime.now()):
            logger.warn('The discount code ' +request.data['discount_code']+' has expired')
            return Response({"message":"زمان استفاده از این کد تخفیف به انمام رسیده است"}
                        ,status=status.HTTP_204_NO_CONTENT)
        if(gift.type=='C'):
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = off_price
            logger.info('The discount code applied and total price of shopping cart changed to '+str(data['discounted_total_cost']))
        if(gift.type == 'A'):
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = (0.8) * (off_price+30000)
            logger.info('The discount code applied and total price of shopping cart changed to '+str(data['discounted_total_cost']))

        else:
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = (0.7) * (off_price+30000)
            logger.info('The discount code applied and total price of shopping cart changed to '+str(data['discounted_total_cost']))

        data['shippingPrice'] = 30000
        return Response(data,status=status.HTTP_200_OK)