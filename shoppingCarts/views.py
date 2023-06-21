from django.shortcuts import render
from .models import *
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import logging
from Backend import dependencies
from products.serializers import *
logger = logging.getLogger("django")

class AddToShoppingCartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        logger.info('request recieved from POST /shoppingCarts/add_to_cart/')
        message = ""
        if(dependencies.shopping_cart_service_instance.create_shopping_cart(request.user , request.data['data'])):
            message = {"message": "محصول مورد نظر به سبد خرید اضافه شد"}
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
            if userCart.user.id == request.user.id:
                if userCart.product.id == int(request.data['data']):
                    userCart.delete()
                    message = {"message": "محصول مورد نظر با موفقیت از سبد خرید حذف شد"}
                    logger.info('product '+str(request.data['data'])+' deleted from shopping cart of user '+str(request.user.id))
                    break
        return Response(status=status.HTTP_200_OK, data=message)


class ShowUserShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logger.info('request recieved from GET /shoppingCarts/show_cart/')
        product_list = dependencies.shopping_cart_service_instance.get_products_of_shop(request.user.id)
        if product_list:
            data = ShoppingCartProductsSerializer(product_list , many = True).data
            response = dependencies.shopping_cart_service_instance.calculate_shopping_cart_info(data)
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class show_checkout_info(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self , request):

        logger.info('request recieved from GET /shoppingCarts/show_checkout_info/')
        data = dependencies.shopping_cart_service_instance.calculate_checkout_info(request.user.id)
        if(data == False):
            return Response({"message":"سبد خرید شما تغییر یافته است"},status=status.HTTP_204_NO_CONTENT)
        logger.info('checkout information of user '+ str(request.user.id)+' returned')
        return Response(data,status=status.HTTP_200_OK)
