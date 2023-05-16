from django.shortcuts import render
from .models import *
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class AddToShoppingCartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        print(request.data)
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
                else:
                    message = {"message": "محصول مورد نظر موجود نیست"}
        return Response(status=status.HTTP_200_OK, data=message)


class DeleteFromShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        message = ""
        for userCart in UserShoppingCart.objects.all():
            if userCart.user_id == request.user.id:
                if userCart.product_id == int(request.data['data']):
                    userCart.delete()
                    message = {"message": "محصول مورد نظر با موفقیت از سبد خرید حذف شد"}
                    break
        return Response(status=status.HTTP_200_OK, data=message)


class ShowUserShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_cart:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data1 = list()
        total_price = 0
        total_price_with_discount = 0
        for i in product_list:
            # print(i[0]['is_deleted'])
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
                # data['inventory'] = i[0]['inventory']
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
        return Response(data2, status=status.HTTP_200_OK)


class show_checkout_info(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self , request):
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
        return Response(data,status=status.HTTP_200_OK)
