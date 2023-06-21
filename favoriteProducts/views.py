from django.shortcuts import render
from products.models import Product
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from Backend import dependencies
import logging
logger = logging.getLogger("django")
# Create your views here.


class AddToFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # logger.info('request recieved from POST /favoriteProducts/add_to_favorite/')
        # message = ""
        # for product in Product.objects.all():
            
        #     if product.pk == int(request.data['data']):
        #         dependencies.favorite_product_service_instance.create_favorite_product(request.user, product)
        #         logger.info('product '+str(product.pk)+' added to favorite list of user '+str(request.user.pk))
        #         message = {"message": "محصول مورد نظر به لیست علاقه مندی ها اضافه شد"}
        #         return Response(status=status.HTTP_200_OK, data=message)
        # logger.warn('product with id'+str(product.pk)+' not found')
        # message = {"message": "محصول مورد نظر در لیست محصولات نیست"}
        # return Response(status=status.HTTP_404_NOT_FOUND, data=message)
            
        return dependencies.add_to_favorite_product_info_service_instance(request)
        

class ShowFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        # logger.info('request recieved from GET /favoriteProducts/show_favorite/')
        # user_favorite_product = list(UserFavoriteProduct.objects.filter(user_id=request.user.id).values())
        # product_list = list()
        # for i in user_favorite_product:
        #     product_list.append(Product.objects.filter(id=i["product_id"]).values())
        # data1 = list()
        # if user_favorite_product:
        #     data1 = dependencies.show_favorite_products_service_instance.show_favorite_products(product_list)
        #     return Response(data1, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)

        return dependencies.show_favorite_product_part_one_info_service_instance.show_favorite_product(request)

class DeleteFromFavoriteProducts(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # logger.info('request recieved from POST /favoriteProducts/delete_from_favorite/')
        # deleted = UserFavoriteProduct.objects.filter(product_id=request.data['data']).delete()
        # if(deleted[0] == 0):
        #     logger.warn('product with id ' +str(request.data['data'])+' has been deleted from product list')
        #     message = {"message": "محصول مورد نظر برای حذف یافت نشد"}
        #     return Response(status=status.HTTP_404_NOT_FOUND, data=message)
        # logger.info('product with id '+str(request.data['data'])+' deleted from favorite list')
        # message = {"message": "محصول مورد نظر با موفقیت از لیست علاقه مندی حذف شد"}
        # return Response(status=status.HTTP_200_OK, data=message)

        return dependencies.delete_from_favorite_product_info_service_instance.delete_from_favorite_product(request)
    

