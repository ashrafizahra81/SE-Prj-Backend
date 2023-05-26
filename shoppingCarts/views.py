from django.shortcuts import render
from .models import *
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import logging
logger = logging.getLogger("django")

class AddToShoppingCartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        logger.info('request recieved from POST /shoppingCarts/add_to_cart/')
        message = ""
        for product in Product.objects.all():
            if product.pk == request.data['data']:
                if product.inventory > 0:
                    cart = UserShoppingCart(
                        user=request.user,
                        product=product
                    )
                    message = {"message": "محصول مورد نظر به سبد خرید اضافه شد"}
                    cart.save()
                    logger.info('product '+str(request.data['data'])+' added to shopping cart of user '+str(request.user.id))
                else:
                    message = {"message": "محصول مورد نظر موجود نیست"}
                    logger.warn('product '+str(request.data['data'])+ ' is not available and could not add to shopping cart')
        return Response(status=status.HTTP_200_OK, data=message)


class DeleteFromShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        logger.info('request recieved from POST /shoppingCarts/delete_from_cart/')
        message = ""
        for userCart in UserShoppingCart.objects.all():
            if userCart.user_id == request.user.id:
                if userCart.product_id == int(request.data['data']):
                    userCart.delete()
                    message = {"message": "محصول مورد نظر با موفقیت از سبد خرید حذف شد"}
                    logger.info('product '+str(request.data['data'])+' deleted from shopping cart of user '+str(request.user.id))
                    break
        return Response(status=status.HTTP_200_OK, data=message)


class ShowUserShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logger.info('request recieved from GET /shoppingCarts/show_cart/')
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_cart:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data1 = list()
        total_price = 0
        total_price_with_discount = 0
        if user_cart:
            for i in product_list:
                if i[0]['is_deleted'] == False:
                    data = {}
                    data['id'] = i[0]['id']
                    data['product_name'] = i[0]['product_name']
                    data['product_size'] = i[0]['product_size']
                    data['product_color'] = i[0]['product_color']
                    data['product_price'] = i[0]['product_price']
                    if int(i[0]['inventory']) > 0:
                        data['is_available'] = True
                    else:
                        data['is_available'] = False
                    data['upload'] = i[0]['upload']
                    data['shop_id'] = i[0]['shop_id']
                    price_off = 0
                    price_off = ((100 - int(i[0]['product_off_percent'])) / 100) * int(i[0]['product_price'])
                    data['product_off_percent'] = price_off
                    total_price += i[0]['product_price']
                    total_price_with_discount += price_off
                    data1.append(data)
            data2 = {}
            data2["products"] = data1
            data2["total_price"] = total_price
            data2["total_price_with_discount"] = total_price_with_discount
            logger.info('products of shopping cart of user '+ str(request.user.id)+' returned')
            return Response(data2, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class show_checkout_info(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self , request):
        logger.info('request recieved from GET /shoppingCarts/show_checkout_info/')
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        off_price = 0
        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            if(product1.is_deleted == 1 or product1.is_available == 0):
                return Response({"message":"سبد خرید شما تغییر یافته است"},status=status.HTTP_204_NO_CONTENT)
            off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
        data={}
        data["discounted_price"] = off_price
        data["total_cost"] = off_price+30000
        data["score"] = int((off_price+30000)/100000)
        data["shippingPrice"] = 30000
        logger.info('checkout information of user '+ str(request.user.id)+' returned')
        return Response(data,status=status.HTTP_200_OK)
