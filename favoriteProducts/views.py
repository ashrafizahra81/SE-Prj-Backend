from django.shortcuts import render
from products.models import Product
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

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
                message = {"message": "محصول مورد نظر به لیست علاقه مندی ها اضافه شد"}

        return Response(status=status.HTTP_200_OK, data=message)


class ShowFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_favorite_product = list(UserFavoriteProduct.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_favorite_product:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data1 = list()
        for i in product_list:
            if i[0]['is_deleted'] == False:
                data = {}
                data['id'] = i[0]['id']
                data['product_name'] = i[0]['product_name']
                # data['product_size'] = i[0]['product_size']
                # data['product_color'] = i[0]['product_color']
                data['product_price'] = i[0]['product_price']
                price_off = 0
                if int(i[0]['product_off_percent']) > 0:
                    price_off = ((100 - int(i[0]['product_off_percent'])) / 100) * int(i[0]['product_price'])
                data['product_off_percent'] = price_off
                # data['is_available'] = i[0]['is_available']
                data['upload'] = i[0]['upload']
                # data['shop_id'] = i[0]['shop_id']
                print(i[0]['product_name'])
                data1.append(data)
        return Response(data1, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteFromFavoriteProducts(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        UserFavoriteProduct.objects.filter(product_id=request.data['data']).delete()
        message = {"message": "محصول مورد نظر با موفقیت از لیست علاقه مندی حذف شد"}
        return Response(status=status.HTTP_200_OK, data=message)

