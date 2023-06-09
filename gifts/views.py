from django.shortcuts import render
from .models import *
from .serializers import *
from accounts.models import User
from shoppingCarts.models import UserShoppingCart
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from Backend import dependencies
import logging
logger = logging.getLogger("django")

class ShowGiftInfo(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self , request):
        logger.info('request recieved from GET /gifts/show_gift/')
        data = []
        for i in Gift.objects.all().values():
            if(datetime(i["date"].year, i["date"].month, i["date"].day) >= datetime.now()):
                gift = GiftInfoSerializer(i)
                data.append(gift.data)
                logger.info('gift with id ' +str(i['id'])+' found')
        if(len(data) == 0):
            logger.warn('No gift is available')
            return Response({"message":"درحال حاضر جایزه‌ای فعال نیست"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data, status=status.HTTP_200_OK)

class GetGift(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self,request):
        logger.info('request recieved from POST /gifts/get_gift/')
        if(type(request.data['score'])== str):
            if(not(request.data['score'].isdigit())):
                logger.warn('format of score entered is not correct')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        gift = Gift.objects.get(score = request.data['score'])
        data = {}
        if(user.score >= gift.score):
            data = dependencies.get_gift_service_instance.get_gifts(request.user, request.data['score'])
            return Response(data, status=status.HTTP_200_OK)
        logger.warn('the score of user '+str(request.user.id)+' is not enough for gift '+str(gift.id))
        return Response({"message":"امتیاز شما کافی نیست"},status=status.HTTP_204_NO_CONTENT)

class ApplyDiscount(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self , request):
        logger.info('request recieved from POST /gifts/apply_discount/')
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        off_price = dependencies.apply_discount_service_instance.cal_total_price_of_shopping_cart(user_cart)

        data={}
        gift = Gift.objects.get(discount_code = request.data['discount_code'])
        if(datetime(gift.date.year, gift.date.month, gift.date.day) < datetime.now()):
            logger.warn('The discount code ' +request.data['discount_code']+' has expired')
            return Response({"message":"زمان استفاده از این کد تخفیف به انمام رسیده است"}
                        ,status=status.HTTP_204_NO_CONTENT)

        data = dependencies.apply_discount_service_instance.check_gift_type(request.data['discount_code'], off_price)
        return Response(data,status=status.HTTP_200_OK)