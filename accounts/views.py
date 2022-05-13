from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from django.core import serializers as srz
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework import status

from permissions import IsOwner

from rest_framework.viewsets import ModelViewSet


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


class ShopsForUser(APIView):
    def get(self, request, pk):
        user_styles = list(UserStyle.objects.filter(user_id_id=pk).values())
        style_id_list = list()
        for item in user_styles:
            style_id_list.append(item['style_id_id'])
        products = list(Product.objects.filter(style_id_id__in=style_id_list).values())
        shop_id_list = list()
        for product in products:
            shop_id_list.append(product['shop_id_id'])
        shops = Shop.objects.filter(pk__in=shop_id_list)
        serialized_data = ShopSerializer(instance=shops, many=True)
        try:
            if shops.count() > 0:
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(serialized_data.errors, status=status.HTTP_417_EXPECTATION_FAILED)


class AddToShoppingCartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        print(request.data)
        for product in Product.objects.all():
            if product.pk == request.data['data'][0]:
                if product.number > 0:
                    cart = UserShoppingCart(
                        user=request.user,
                        product=product
                    )
                cart.save()
        return Response(status=status.HTTP_200_OK)


class DeleteFromShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        UserShoppingCart.objects.filter(product_id=request.data['data'][0]).delete()
        return Response(status=status.HTTP_200_OK)


class ShowUserShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user_cart = list(UserShoppingCart.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_cart:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data = {}
        data['image'] = product_list[0][0]['image']
        data['name'] = product_list[0][0]['name']
        data['price'] = product_list[0][0]['price']
        data['shop_id_id'] = product_list[0][0]['shop_id_id']
        print(product_list[0][0]['name'])
        return Response(data, status=status.HTTP_200_OK)

class AddToFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        for product in Product.objects.all():
            if product.pk == request.data['data'][0]:
                favorite_product = UserFavoriteProduct(
                    user=request.user,
                    product=product
                )
                favorite_product.save()

        return Response(status=status.HTTP_200_OK)


class ShowFavoriteProduct(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_favorite_product = list(UserFavoriteProduct.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_favorite_product:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data = {}
        data['image'] = product_list[0][0]['image']
        data['name'] = product_list[0][0]['name']
        data['price'] = product_list[0][0]['price']
        data['shop_id_id'] = product_list[0][0]['shop_id_id']
        print(product_list[0][0]['name'])
        return Response(data, status=status.HTTP_200_OK)

##########################################Sprint3#########################################3

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
            data['shop_phone_num'] = shop_manager.shop_phone_num
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

# class CheckoutShoppingCart


# class CreateShopViewSet(ModelViewSet):
#     queryset = Shop.objects.none()
#     serializer_class = CreateShopSerializer
#     permission_classes = (IsAuthenticated,)
#     http_method_names = ['post', ]
#
#     def create(self, request, *args, **kwargs):
#         user = request.user
#         _serializer = self.serializer_class(data=request.data)
#
#         if _serializer.is_valid():
#             _serializer.save(user=user)
#             return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
#         else:
#             return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA



# class ShopManagerRegistrationAndCreateShop(APIView):
#     def post(self, request):
#         serialized_data = ShopManagerRegistrationAndCreateShopSerializer(data=request.data)
#         data = {}
#         if serialized_data.is_valid():
#             shop = serialized_data.save()
#             data['username'] = shop.username
#             data['email'] = shop.email
#             data['password'] = shop.password
#             data['user_phone_number'] = shop.user_phone_number
#             data['shop_name'] = shop.shop_name
#             data['shop_description'] = shop.shop_description
#             data['shop_address'] = shop.shop_address
#             data['shop_phone_num'] = shop.shop_phone_num
#             refresh = RefreshToken.for_user(shop)
#             data['refresh'] = str(refresh)
#             data['access'] = str(refresh.access_token)
#
#             user = User.objects.all()
#             for u in user:
#                 print(u.password)
#             return Response(data)
#         return Response(serialized_data.errors)
#
#
#

# class AddProductsToShopView(APIView):
#     permission_classes = [IsAuthenticated,]
#     data = {}
#     def post(self, request):
#         #shop = Shop.objects.get(shop_owner = request.user)
#         serialized_data = ProductsSerializer(data = request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data , status=status.HTTP_201_CREATED)
#         return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

#





