from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from datetime import datetime


class UserRegister(APIView):
    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            account = serialized_data.save()
            # data['response'] = "successfully registered"
            data['username'] = account.username
            data['email'] = account.email
            data['user_phone_number'] = account.user_phone_number
            refresh = RefreshToken.for_user(account)
            # res = {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # }
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            # data['user_postal_code'] = account.user_postal_code
            # data['user_address'] = account.user_address
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            return Response(data)
        return Response(serialized_data.errors)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class UserEditProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serialized_data = UserEditProfileSerializer(instance=user, data=request.data, partial=True)
        if serialized_data.is_valid():
            # print(request.user.email)
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStyles(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_styles = list(UserStyle.objects.filter(user_id=request.user.id).values())
        style_id_list = list()
        for item in user_styles:
            style_id_list.append(item['style_id_id'])
        styles = list(Style.objects.filter(pk__in=style_id_list).values('style_image_url'))
        if styles:
            return JsonResponse(styles, safe=False)
        else:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)


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
        UserShoppingCart.objects.filter(product_id=request.data['data']).delete()
        message = {"message": "محصول مورد نظر با موفقیت از سبد خرید حذف شد"}
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
        for i in product_list:
            data = {}
            data['id'] = i[0]['id']
            data['product_name'] = i[0]['product_name']
            data['product_description'] = i[0]['product_description']
            data['product_price'] = i[0]['product_price']
            if int(i[0]['inventory']) > 0:
                data['is_available'] = True
            else:
                data['is_available'] = False
            # data['inventory'] = i[0]['inventory']
            data['upload'] = i[0]['upload']
            data['shop_id'] = i[0]['shop_id']
            total_price += i[0]['product_price']
            data1.append(data)
        data1.append({"total_price": total_price})
        return Response(data1, status=status.HTTP_200_OK)


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
            data = {}
            data['id'] = i[0]['id']
            data['product_name'] = i[0]['product_name']
            data['product_description'] = i[0]['product_description']
            data['product_price'] = i[0]['product_price']
            data['is_available'] = i[0]['is_available']
            data['upload'] = i[0]['upload']
            data['shop_id'] = i[0]['shop_id']
            print(i[0]['product_name'])
            data1.append(data)
        return Response(data1, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)


class ShopManagerRegister(APIView):
    def post(self, request):
        serialized_data = ShopManagerRegisterSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            shop_manager = serialized_data.save()
            # data['response'] = "successfully registered"
            data['username'] = shop_manager.username
            data['email'] = shop_manager.email
            data['user_phone_number'] = shop_manager.user_phone_number
            data['shop_name'] = shop_manager.shop_name
            data['shop_description'] = shop_manager.shop_description
            data['shop_address'] = shop_manager.shop_address
            data['shop_phone_number'] = shop_manager.shop_phone_number
            refresh = RefreshToken.for_user(shop_manager)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return Response(data)
        return Response(serialized_data.errors)


class EditShop(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serialized_data = EditShopSerializer(instance=user, data=request.data, partial=True)
        if serialized_data.is_valid():
            # print(request.user.email)
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductsToShopViewSet(ModelViewSet):
    queryset = Product.objects.none()
    serializer_class = ProductsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        _serializer = self.serializer_class(data=request.data)

        if _serializer.is_valid():
            _serializer.save(shop=request.user)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA


class EditProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serialized_data = EditProductSerializer(instance=product, data=request.data, partial=True)
        if serialized_data.is_valid():
            # print(request.user.email)
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'product deleted'})


class GetProductInfo(APIView):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product:
            serialized_data = ProductsSerializer(instance=product, data=request.data, partial=True)
            if serialized_data.is_valid():
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized_data.errors, status=status.HTTP_417_EXPECTATION_FAILED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetUserOrders(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):

        user_orders = list(Order.objects.filter(user_id=request.user.id).values())
        data = list()
        for o in user_orders:
            print(o)
            product = Product.objects.get(pk=o['product_id'])
            serialized_product = ProductInfoSerializer(instance=product)
            js = serialized_product.data
            js['cost'] = o['cost']
            js['order_date'] = o['order_date']
            js['complete_date'] = o['complete_date']
            js['status'] = o['status']
            data.append(js)
        if data:
            return JsonResponse(data, safe=False)
        else:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class DeleteFromFavoriteProducts(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        UserFavoriteProduct.objects.filter(product_id=request.data['data']).delete()
        message = {"message": "محصول مورد نظر با موفقیت از لیست علاقه مندی حذف شد"}
        return Response(status=status.HTTP_200_OK, data=message)


class CheckoutShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):

        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        data = list()
        price = 0
        date_of_buy = datetime.now()
        user_buyer = {}
        user_buyer["buyer"] = request.user.email
        data.append(user_buyer)

        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            price += product1.product_price

        for o in user_cart:
            product = Product.objects.get(pk=o['product_id'])
            serialized_product = ProductInfoSerializer(instance=product)
            js = serialized_product.data
            c = Order(
                user=request.user,
                product=product,
                cost=price,
                status="Accepted",
            )
            c.save()
            js['product'] = product.product_price
            data.append(js)
            UserShoppingCart.objects.filter(user_id=request.user.id).delete()

        # print(price)
        dict_price = {}
        dict_price["total price"] = price
        date = {}
        date["date"] = date_of_buy
        data.append(dict_price)
        data.append(date)
        # print(data)
        if data:
            return JsonResponse(data, safe=False)
        return Response(data, status=status.HTTP_201_CREATED)
