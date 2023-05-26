from django.shortcuts import render
from products.models import Product
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import logging
logger = logging.getLogger("django")
# Create your views here.


class AddToFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        message = ""
        for product in Product.objects.all():
            if product.pk == request.data['data']:
                favorite_product = UserFavoriteProduct(
                    user=request.user,
                    product=product
                )
                favorite_product.save()
                logger.info('product '+str(product.pk)+' added to favorite list of user '+str(request.user.pk))
                message = {"message": "محصول مورد نظر به لیست علاقه مندی ها اضافه شد"}
                return Response(status=status.HTTP_200_OK, data=message)
        logger.warn('product with id'+str(product.pk)+' not found')
        message = {"message": "محصول مورد نظر در لیست محصولات نیست"}
        return Response(status=status.HTTP_404_NOT_FOUND, data=message)
            
        


class ShowFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_favorite_product = list(UserFavoriteProduct.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_favorite_product:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data1 = list()
        if user_favorite_product:
            for i in product_list:
                if i[0]['is_deleted'] == False:
                    logger.info('product with id ' +str(i[0]['id'])+' from favorite list found')
                    data = {}
                    data['id'] = i[0]['id']
                    data['product_name'] = i[0]['product_name']
                    data['product_price'] = i[0]['product_price']
                    price_off = 0
                    if int(i[0]['product_off_percent']) > 0:
                        price_off = ((100 - int(i[0]['product_off_percent'])) / 100) * int(i[0]['product_price'])
                    data['product_off_percent'] = price_off
                    data['upload'] = i[0]['upload']
                    data1.append(data)
                logger.warn('product with id ' +str(i[0]['id'])+' has been deleted from product list')
            return Response(data1, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteFromFavoriteProducts(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        deleted = UserFavoriteProduct.objects.filter(product_id=request.data['data']).delete()
        if(deleted[0] == 0):
            logger.warn('product with id ' +str(request.data['data'])+' has been deleted from product list')
            message = {"message": "محصول مورد نظر برای حذف یافت نشد"}
            return Response(status=status.HTTP_404_NOT_FOUND, data=message)
        logger.info('product with id '+str(request.data['data'])+' deleted from favorite list')
        message = {"message": "محصول مورد نظر با موفقیت از لیست علاقه مندی حذف شد"}
        return Response(status=status.HTTP_200_OK, data=message)

