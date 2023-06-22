from django.shortcuts import render
from accounts.models import User
from shoppingCarts.models import UserShoppingCart
from favoriteProducts.models import UserFavoriteProduct
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from permissions import IsShopOwner, IsShopManager
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
import logging
from Backend import dependencies
logger = logging.getLogger("django")

class EditProduct(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]

    def put(self, request, pk):
        logger.info('request recieved from PUT /products/edit_product/<int:pk>/')
        product = Product.objects.get(pk=pk)
        self.check_object_permissions(request, product)
        result = dependencies.update_product_from_editing_service_instance.update_product(pk , request.data)
        if(result == True):
            return Response(status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]

    def delete(self, request, pk):
        logger.info('request recieved from DELETE /products/delete_product/<int:pk>/')
        product = Product.objects.get(pk=pk)
        self.check_object_permissions(request, product)
        dependencies.update_product_after_deleting_service_instance.update_product(pk , request)
        logger.info('product with id '+str(product.pk)+' deleted')
        return Response({'message': 'محصول موردنظر با موفقیت حذف شد'}, status=status.HTTP_200_OK)


class GetProductInfo(APIView):

    def get(self, request, pk):
        logger.info('request recieved from GET /products/product_info/<int:pk>/')
        product = Product.objects.get(pk=pk)
        logger.info('product with id '+str(product.pk)+' found')
        if product and product.is_deleted == False:
            data = ShowProductsSerializer(product , context={'user_id': request.user.id})
            return Response(data.data, status=status.HTTP_200_OK)
        logger.info('product with id '+str(product.pk)+' is deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddProductsToShopViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsShopManager)
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        logger.info('request recieved from POST /products/add_products_to_shop/')
        self.check_object_permissions(request, request.user)
        data = dependencies.create_product_service_instance.create_product(request.data , request.user.id)    
        if(data[0]):
            return Response(data=data[1].data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            logger.warn('dara entered is not valid')
            return Response(data=data[1], status=status.HTTP_400_BAD_REQUEST)  # NOQA


class ShowProductsByShop(APIView):
    
    permission_classes = (IsAuthenticated, IsShopManager)

    def get(self, request):
        logger.info('request recieved from GET /products/show_products_of_shop/')
        self.check_object_permissions(request, request.user)
        product_list = list(Product.objects.filter(shop=request.user.id , is_deleted=False).values())
        shop = User.objects.get(id = request.user.id)
        data = ProductOfShopSerializer(product_list , many = True).data
        if len(data) == 0:
            logger.info('shop '+str(request.user.id)+' has no products')
        data = dependencies.show_products_of_shop_service_instance.get_shop_info(shop , data)
        logger.info('products of shop '+str(shop.id)+' found')
        return Response(data, status=status.HTTP_200_OK)


class ShowAllProducts(APIView):
    def get(self, request):
        logger.info('request recieved from GET /products/show_all_products/')
        product_list = list(Product.objects.filter(is_deleted=False).values())
        data = ProductOfShopSerializer(product_list , many = True).data
        data1 = []
        for i in data:
            data1.append(dict(i))
        if len(data1) == 0:
            logger.info('There is no product')
        logger.info('products of all shops found')
        return Response(data1, status=status.HTTP_200_OK)



class Report(APIView):
    permission_classes = [IsAuthenticated, IsShopManager]
    
    def get(self , request):
        logger.info('request recieved from GET /products/report/')
        self.check_object_permissions(request, request.user)
        product_list = list(Product.objects.filter(shop=request.user.id , is_deleted=False).values())
        data = ReportSerializer(product_list , many =True).data
        data1=[]
        for i in data:
            data1.append(dict(i))
        totalPriceOfShop = dependencies.show_products_of_shop_service_instance.calculate_total_price(product_list)
        data1.append({'totalSell':totalPriceOfShop})
        logger.info('report of shop '+str(request.user.id)+' returned')
        return Response(data1, status=status.HTTP_200_OK)


class Filters(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        logger.info('request recieved from POST /products/filters/')
        filter = request.data['group'][0]
        data = dependencies.filter_product_service_instance.filter_product(filter)
        if(len(data) > 0):
            logger.info('products with filter '+filter+' found')
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            logger.info('no products with filter '+filter+' found')
            return Response(status=status.HTTP_204_NO_CONTENT)