from django.shortcuts import render
from .models import *
from shoppingCarts.models import UserShoppingCart
from products.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

class ChargeWallet(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self , request):
        wallet = Wallet.objects.get(user=request.user)
        data2 = request.data
        data = {}
        if(data2['insert'] == '' or data2['insert'] < 0 or data2['insert'] == 0):
            data={"message": "مقدار وارد شده قابل قبول نیست"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        wallet.balance += float(data2['insert'])
        wallet.save()
        data['balance'] = wallet.balance
        return Response(data, status=status.HTTP_200_OK)

class BuyFromWallet(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self , request):
        AllUserShoppingCart_list = list(UserShoppingCart.objects.all().values())
        UserShoppingCart_list = []
        UserShoppingCartProductId_list = []
        print(AllUserShoppingCart_list)
        data = {}
        totalPrice = 0
        for userShoppingCart in AllUserShoppingCart_list:
            if userShoppingCart['user_id'] == request.user.id:
                if userShoppingCart['status'] == "not Accepted":
                    UserShoppingCart_list.append(userShoppingCart)
                    UserShoppingCartProductId_list.append(userShoppingCart['product_id'])
        

        
        print(len(UserShoppingCart_list))
        print(len(UserShoppingCartProductId_list))

        products_list = list(Product.objects.all().values())
        while len(UserShoppingCartProductId_list) > 0:
            for product in products_list:
                if UserShoppingCartProductId_list[0] == product['id']:
                    totalPrice += product['product_price']
                    UserShoppingCartProductId_list.pop(0)
                    break

        wallet = Wallet.objects.get(user=request.user)

        if totalPrice > 0: 

            if wallet.balance >= totalPrice:
                wallet.balance -= totalPrice
                data['status'] = 'done!'
                for userShoppingCart in AllUserShoppingCart_list:
                    if userShoppingCart['user_id'] == request.user.id:
                        if userShoppingCart['status'] == "not Accepted":
                            UserShoppingCartById = UserShoppingCart.objects.get(id=userShoppingCart['id'])
                            UserShoppingCartById.status = "Accepted"
                            UserShoppingCartById.save()

                wallet.save()

            else:
                data['status'] = 'Your account balance is insufficient!'
        
        else:
            data['status'] = "there are no items in your shopping cart"
   

        
        return Response(data, status=status.HTTP_200_OK)

