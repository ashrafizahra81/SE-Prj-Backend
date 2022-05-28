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

        a = Style.objects.filter(pk__in=style_id_list).values()
        products = []
        for i in list(a):
            if i['product_id']:
                product = Product.objects.get(pk=i['product_id'])
                ser = ProductsSerializer(instance=product).data
                ser['upload'] = i['style_image_url']
                products.append(ser)
            else:
                products.append({'upload': i['style_image_url']})

        return Response(data=products, status=status.HTTP_200_OK)


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
            data['product_size'] = i[0]['product_size']
            data['product_color'] = i[0]['product_color']
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
        data1 = {}
        data1['username'] = user.username
        data1['user_phone_number'] = user.user_phone_number
        data1['email'] = user.email
        data1['shop_address'] = user.shop_address
        data1['shop_name'] = user.shop_name
        data1['shop_phone_number'] = user.shop_phone_number
        serialized_data = EditShopSerializer(data=request.data, instance=user, partial=True)
        data = {}
        if serialized_data.is_valid():

            edited_shop = serialized_data.save()

            if data1['username'] != edited_shop.username:
                data['username'] = edited_shop.username
            else:
                data['username'] = ""

            if data1['user_phone_number'] != edited_shop.user_phone_number:
                data['user_phone_number'] = edited_shop.user_phone_number
            else:
                data['user_phone_number'] = ""

            if data1['email'] != edited_shop.email:
                data['email'] = edited_shop.email
            else:
                data['email'] = ""

            if data1['shop_address'] != edited_shop.shop_address:
                data['shop_address'] = edited_shop.shop_address
            else:
                data['shop_address'] = ""

            if data1['shop_name'] != edited_shop.shop_name:
                data['shop_name'] = edited_shop.shop_name
            else:
                data['shop_name'] = ""

            if data1['shop_phone_number'] != edited_shop.shop_phone_number:
                data['shop_phone_number'] = edited_shop.shop_phone_number
            else:
                data['shop_phone_number'] = ""

            return Response(data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductsToShopViewSet(ModelViewSet):
    queryset = Product.objects.none()
    serializer_class = ProductAndStyleSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        _serializer = self.serializer_class(data=request.data)
        data = {}

        print(_serializer)
        if _serializer.is_valid():
            data = request.data
            print(data['upload'])
            # print(p.shop_id)
            data1 = {}
            product = Product(
                shop_id=request.user,
                product_name=data['product_name'],
                product_price=data['product_price'],
                product_size=data['product_size'],
                product_height=data['product_height'],
                product_design=data['product_design'],
                product_material=data['product_material'],
                product_country=data['product_country'],
                product_off_percent=data['product_off_percent'],
                inventory=data['inventory'],
                upload=data['upload'],
            )
            product.save()
            data1['product_name'] = data['product_name']
            data1['product_price'] = data['product_price']
            data1['product_size'] = data['product_size']
            data1['product_height'] = data['product_height']
            data1['product_design'] = data['product_design']
            data1['product_material'] = data['product_material']
            data1['product_country'] = data['product_country']
            data1['inventory'] = data['inventory']
            s = Style(product=product,
                      style_param_1=data['style_param_1'],
                      style_param_2=data['style_param_2'],
                      style_param_3=data['style_param_3'],
                      style_param_4=data['style_param_4'],
                      style_param_5=data['style_param_5']
                      )
            s.save()
            return Response(data=data1, status=status.HTTP_201_CREATED)  # NOQA
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
                ret_val = serialized_data.data
                is_fav = UserFavoriteProduct.objects.filter(user_id=request.user.id, product_id=product.pk).exists()
                in_cart = UserShoppingCart.objects.filter(user_id=request.user.id, product_id=product.pk).exists()
                ret_val['is_favorite'] = is_fav
                ret_val['is_in_cart'] = in_cart
                return Response(ret_val, status=status.HTTP_200_OK)
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


class ShowProductsByShop(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        product_list = list(Product.objects.filter(shop=request.data['data']).values())
        data = {}
        data1 = list()
        for i in product_list:
            data = {}
            data['id'] = i['id']
            data['product_name'] = i['product_name']
            data['product_size'] = i['product_size']
            data['product_color'] = i['product_color']
            data['product_price'] = i['product_price']
            data['inventory'] = i['inventory']
            data['upload'] = i['upload']
            data['shop_id'] = i['shop_id']
            data1.append(data)
        return Response(data1, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)


class AddOrDeleteFavoriteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        is_fav = UserFavoriteProduct.objects.filter(user_id=request.user.id, product_id=request.data['data']).exists()
        print(is_fav)
        if is_fav:
            user_product = UserFavoriteProduct.objects.get(user_id=request.user, product_id=request.data['data'])
            user_product.delete()
            message = "محصول مورد نظر از لیست علاقه مندی ها حذف شد"
        else:
            to_save = UserFavoriteProduct(user=request.user, product=Product.objects.get(pk=request.data['data']))
            to_save.save()
            message = "محصول مورد نظر به لیست علاقه مندی ها اضافه شد"

        return Response(status=status.HTTP_200_OK, data=message)


class AddOrRemoveShoppingCartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        in_cart = UserShoppingCart.objects.filter(user_id=request.user.id, product_id=request.data['data']).exists()
        if in_cart:
            user_product = UserShoppingCart.objects.get(user_id=request.user.id, product_id=request.data['data'])
            user_product.delete()
            message = "محصول مورد نظر از سبد خرید حذف شد"
        else:
            to_save = UserShoppingCart(user=request.user, product=Product.objects.get(pk=request.data['data']),
                                       status="NOT PAID")
            to_save.save()
            message = "محصول مورد نظر به سبد خرید اضافه شد"

        return Response(status=status.HTTP_200_OK, data=message)
