from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from permissions import IsShopOwner
from django.core.files.storage import FileSystemStorage
import requests
import json
import string
from questions import ai_similarity
from questions.models import UserMoreQuestions
import numpy as np


class CreateRecSystem(APIView):
    rec_system = None

    def post(self, request):

        if self.rec_system is None:
            features = np.zeros((100, 5, 3))

            cls = list(Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                                  'style_param_5'))

            clothes = [item for item in cls]
            for i in range(100):
                lst = list(clothes[i].values())
                for j in range(5):
                    val = [int(x) for x in lst[j].split(',')]
                    for k in range(3):
                        features[i][j][k] = val[k]

            self.rec_system = ai_similarity.RecommendationSystem(features)
        else:
            pass

        return Response(status=status.HTTP_200_OK)


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

            mail_subject = 'ثبت نام در سبکینو'
            message = 'ثبت نام شما در سایت سبکینو با موفقیت انجام شد!'
            to_email = account.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return Response(data)
        return Response(serialized_data.errors)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """

    serializer_class = CustomTokenVerifySerializer


class UserEditProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        print(user.username)
        data1 = {}

        data1['email'] = user.email
        data1['username'] = user.username
        data1['user_phone_number'] = user.user_phone_number
        data1['user_postal_code'] = user.user_postal_code
        data1['user_address'] = user.user_address

        data = {}

        serialized_data = UserEditProfileSerializer(instance=user, data=request.data, partial=True)
        if serialized_data.is_valid():
            # print(request.user.email)
            edited_user = serialized_data.save()

            if data1['email'] != edited_user.email:
                data['email'] = edited_user.email
            else:
                data['email'] = ""

            if data1['username'] != edited_user.username:
                data['username'] = edited_user.username
            else:
                data['username'] = ""

            if data1['user_phone_number'] != edited_user.user_phone_number:
                data['user_phone_number'] = edited_user.user_phone_number
            else:
                data['user_phone_number'] = ""

            if data1['user_postal_code'] != edited_user.user_postal_code:
                data['user_postal_code'] = edited_user.user_postal_code
            else:
                data['user_postal_code'] = ""

            if data1['user_address'] != edited_user.user_address:
                data['user_address'] = edited_user.user_address
            else:
                data['user_address'] = ""

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


class UserMoreStylesView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_styles = list(UserMoreStyles.objects.filter(user_id=request.user.id).values())
        style_id_list = list()
        for item in user_styles:
            style_id_list.append(item['style_id'])

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
        total_price_with_discount = 0
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


class ShopManagerRegister(APIView):
    def post(self, request):
        serialized_data = ShopManagerRegisterSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            shop_manager = serialized_data.save()
            # data['response'] = "successfully registered"
            data['username'] = shop_manager.username
            data['email'] = shop_manager.email
            # data['user_phone_number'] = shop_manager.user_phone_number
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

    def post(self, request):
        user = User.objects.get(id=request.user.id)
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

            return Response(serialized_data.data, status=status.HTTP_200_OK)
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
            data2 = request.data

            # m = request.FILES['upload']
            # fs = FileSystemStorage('uploads/')
            # filename = fs.save(m.name, m)
            # upload_url_file = fs.url(filename)
            # print(upload_url_file)
            #
            # with open(f'./uploads{upload_url_file}', 'rb') as f:
            #     data = f.read()
            # r = requests.post("https://api.nft.storage/upload", headers={
            #     'accept': 'application/json',
            #     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEYwOEQxYmYyZEREMGNBMGM2Qzc1NENEOUMyMDFBY2NCOGUxMzNmN2EiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1MzcwODczOTg5MCwibmFtZSI6ImtleSJ9.vBoLYYzJSLqnLuqWVXWIJEZbEm8SqyfhSWKb-yPl-h8',
            #     'Content-Type': 'image/*'},
            #                   data=data)
            # print(json.loads(r.text))
            # str = json.loads(r.text)['value']['cid'].translate({ord(c): None for c in string.whitespace})
            # print(str)
            # str2 = "https://ipfs.io/ipfs/" + str
            # print(str2)

            # print(p.shop_id)
            data1 = {}
            product = Product(

                shop=request.user,
                product_name=data2['product_name'],
                product_price=data2['product_price'],
                product_size=data2['product_size'],
                product_group=data2['product_group'],
                product_image=data2['product_image'],
                product_color=data2['product_color'],
                product_height=data2['product_height'],
                product_design=data2['product_design'],
                product_material=data2['product_material'],
                product_country=data2['product_country'],
                # product_off_percent=data2['product_off_percent'],
                inventory=data2['inventory'],
                # upload=str2,
                is_available=True,
            )
            product.save()
            data1['product_id'] = product.id
            data1['product_name'] = data2['product_name']
            data1['product_price'] = data2['product_price']
            data1['product_size'] = data2['product_size']
            data1['product_group'] = data2['product_group']
            data1['product_image'] = data2['product_image']
            data1['product_color'] = data2['product_color']
            data1['product_height'] = data2['product_height']
            data1['product_design'] = data2['product_design']
            data1['product_material'] = data2['product_material']
            data1['product_country'] = data2['product_country']
            data1['inventory'] = data2['inventory']
            # data1['upload'] = str2
            s = Style(product=product,
                      style_image_url=data1['product_image'],
                      style_param_1=data2['style_param_1'],
                      style_param_2=data2['style_param_2'],
                      style_param_3=data2['style_param_3'],
                      style_param_4=data2['style_param_4'],
                      style_param_5=data2['style_param_5']
                      )
            s.save()
            return Response(data=data1, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA


class EditProduct(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        self.check_object_permissions(request, product)

        data1 = {}
        data1['product_name'] = product.product_name
        data1['product_price'] = product.product_price
        data1['inventory'] = product.inventory
        data1['product_size'] = product.product_size
        data1['product_color'] = product.product_color
        data1['product_height'] = product.product_height
        data1['product_design'] = product.product_design
        data1['product_material'] = product.product_material
        data1['product_country'] = product.product_country
        data1['product_off_percent'] = product.product_off_percent
        data1['is_available'] = product.is_available

        data = {}

        serialized_data = EditProductSerializer(instance=product, data=request.data, partial=True)
        if serialized_data.is_valid():
            # print(request.user.email)
            edited_product = serialized_data.save()

            if data1['product_name'] != edited_product.product_name:
                data['product_name'] = edited_product.product_name
            else:
                data['product_name'] = ""

            if data1['product_price'] != edited_product.product_price:
                data['product_price'] = edited_product.product_price
            else:
                data['product_price'] = ""

            if data1['inventory'] != edited_product.inventory:
                data['inventory'] = edited_product.inventory
            else:
                data['inventory'] = ""

            if data1['product_size'] != edited_product.product_size:
                data['product_size'] = edited_product.product_size
            else:
                data['product_size'] = ""

            if data1['product_color'] != edited_product.product_color:
                data['product_color'] = edited_product.product_color
            else:
                data['product_color'] = ""

            if data1['product_height'] != edited_product.product_height:
                data['product_height'] = edited_product.product_height
            else:
                data['product_height'] = ""

            if data1['product_design'] != edited_product.product_design:
                data['product_design'] = edited_product.product_design
            else:
                data['product_design'] = ""

            if data1['product_material'] != edited_product.product_material:
                data['product_material'] = edited_product.product_material
            else:
                data['product_material'] = ""

            if data1['product_country'] != edited_product.product_country:
                data['product_country'] = edited_product.product_country
            else:
                data['product_country'] = ""

            if data1['product_off_percent'] != edited_product.product_off_percent:
                data['product_off_percent'] = edited_product.product_off_percent
            else:
                data['product_off_percent'] = ""

            if data1['is_available'] != edited_product.is_available:
                data['is_available'] = edited_product.is_available
            else:
                data['is_available'] = ""

            return Response(data, status=status.HTTP_200_OK)
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
            serialized_product = ProductsSerializer(instance=product)
            js = serialized_product.data
            print('upload')
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
        off_price = 0
        product_inventory = 0
        date_of_buy = datetime.now()
        user_buyer = {}
        user_buyer["buyer"] = request.user.email
        # data.append(user_buyer)
        p_data = {}

        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            product_inventory = product1.inventory - 1
            print(product_inventory)
            p_data['inventory'] = product_inventory
            json_object = json.dumps(p_data, indent=4)
            print(p_data)
            serialized_data = EditProductSerializer(instance=product1, data=p_data, partial=True)
            if product1.product_off_percent != 0:
                off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
            if serialized_data.is_valid():
                edited_product = serialized_data.save()
            else:
                print("not valid")
            price += product1.product_price

        for o in user_cart:
            product = Product.objects.get(pk=o['product_id'])
            serialized_product = ProductInfoSerializer(instance=product)
            js = serialized_product.data
            c = Order(
                user=request.user,
                product=product,
                cost=product.product_price,
                total_cost=price,
                off_cost=off_price,
                status="Accepted",
            )
            c.save()
            js['product'] = product.product_price
            data.append(js)
            UserShoppingCart.objects.filter(user_id=request.user.id).delete()

        # print(price)
        dict_price = {}
        dict_price["total price"] = price
        dict_price["total off_price"] = off_price
        date = {}
        date["date"] = date_of_buy
        data.append(dict_price)
        data.append(date)
        # print(data)
        if data:
            return JsonResponse(data, safe=False)
        return Response(data, status=status.HTTP_201_CREATED)


class ShowProductsByShop(APIView):

    def post(self, request):
        product_list = list(Product.objects.filter(shop=request.data['id']).values())
        shop = User.objects.filter(id=request.data['data']).values()
        print(shop)
        data = {}
        data1 = list()
        for i in product_list:
            data = {}
            data['id'] = i['id']
            data['product_name'] = i['product_name']
            # data['product_size'] = i['product_size']
            # data['product_color'] = i['product_color']
            data['product_price'] = i['product_price']
            price_off = 0
            if int(i['product_off_percent']) > 0:
                price_off = ((100 - int(i['product_off_percent'])) / 100) * int(i['product_price'])
            data['product_off_percent'] = price_off
            data['inventory'] = i['inventory']
            data['upload'] = i['upload']
            data['shop_id'] = i['shop_id']
            data1.append(data)
        data2 = {}
        data2["products"] = data1
        data2["shop_name"] = shop[0]['shop_name']
        data2["shop_address"] = shop[0]['shop_address']
        data2["shop_phone_number"] = shop[0]['shop_phone_number']
        return Response(data2, status=status.HTTP_200_OK)
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


class ShowAllProducts(APIView):
    def get(self, request):
        product_list = list(Product.objects.all().values())
        data = {}
        data1 = list()
        print(product_list)
        for i in product_list:
            data = {}
            print(1)
            print(i['id'])
            print(2)
            data['id'] = i['id']
            data['product_name'] = i['product_name']
            data['product_price'] = i['product_price']
            price_off = 0
            if int(i['product_off_percent']) > 0:
                price_off = ((100 - int(i['product_off_percent'])) * i['product_price']) / 100
            data['product_off_percent'] = price_off
            data['inventory'] = i['inventory']
            data['upload'] = i['upload']
            data['shop_id'] = i['shop_id']
            data1.append(data)
        return Response(data1, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowUserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        print(user.username)
        data = {}
        if user.shop_name == None:
            data['email'] = user.email
            data['username'] = user.username
            data['user_phone_number'] = user.user_phone_number
            data['user_postal_code'] = user.user_postal_code
            data['user_address'] = user.user_address
        else:
            data['email'] = user.email
            data['username'] = user.username
            data['shop_name'] = user.shop_name
            data['shop_phone_number'] = user.shop_phone_number
            data['user_phone_number'] = user.user_phone_number
            data['shop_address'] = user.shop_address

        return Response(data, status=status.HTTP_200_OK)


class Logout(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowOrdersToShop(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        order_list = list(Order.objects.all().values())
        product_list = list()
        for order in order_list:
            # print(order)
            for product in Product.objects.all().values():
                print(product['id'])
                if product['id'] == order['product_id']:

                    if product['shop_id'] == request.user.id:
                        data = {}
                        data['id'] = product['id']
                        data['product_name'] = product['product_name']
                        data['product_size'] = product['product_size']
                        data['product_color'] = product['product_color']
                        data['product_price'] = product['product_price']
                        data['inventory'] = product['inventory']
                        data['upload'] = product['upload']
                        data['shop_id'] = product['shop_id']
                        product_list.append(data)
        return Response(product_list, status=status.HTTP_200_OK)


class PopularProducts(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # user = User.objects.get(id=request.user.id)
        product = Product.objects.get(pk=request.data['data'][0])
        product_score = request.data['data'][1]
        print(product_score)
        score = product_score + product.score

        s = ProductScore(user_id=request.user.id,
                         product=product,
                         score=score
                         )
        s.save()

        print(score)
        # product_number_of_votes = request.data['data'][1],
        nums_of_votes = product.number_of_votes + 1
        data = {}
        data['number_of_votes'] = nums_of_votes
        if nums_of_votes != 0:
            data['score'] = float(score / nums_of_votes)
        else:
            data['score'] = 0.0
        print(data)
        print("**********")
        json_object = json.dumps(data, indent=4)
        print(json_object)
        print("///////////////////")
        serialized_data = EditProductSerializer(data=data, instance=product, partial=True)
        print(serialized_data)
        if serialized_data.is_valid():
            edited_shop = serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowPopularProduct(APIView):
    def get(self, request):
        row = 0
        for i in Product.objects.all():
            row = row + 1
        table = [[0 for c in range(3)] for r in range(row)]
        j = 0
        for i in Product.objects.all().values():
            table[j][0] = i['id']
            table[j][1] = float(i['score'])
            table[j][2] = int(i['number_of_votes'])
            j = j + 1
        data1 = list()
        j = 0
        for i in ai_similarity.RecommendationSystem.favorite_items(table):
            product = Product.objects.filter(id=i[0]).values()
            data = {}
            data['id'] = product[0]['id']
            # print(product.pk)
            data['product_name'] = product[0]['product_name']
            # data['product_size'] = product['product_size']
            # data['product_color'] = product['product_color']
            data['product_price'] = product[0]['product_price']
            price_off = 0
            if product[0]['product_off_percent'] > 0:
                price_off = ((100 - product[0]['product_off_percent']) / 100) * product[0]['product_price']
            data['product_off_percent'] = price_off
            # data['inventory'] = i['inventory']
            data['upload'] = product[0]['upload']
            data['shop_id'] = product[0]['shop_id']
            data1.append(data)
        print(data1)
        return Response(data1, status=status.HTTP_200_OK)


class MoreQuestions(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user_more_questions = UserMoreQuestions.objects.get(user_id=request.user.id)
        new_list = list()

        new_list.append(float(user_more_questions.answer_1))
        new_list.append(float(user_more_questions.answer_2))
        new_list.append(float(user_more_questions.answer_3))
        new_list.append(float(user_more_questions.answer_4))
        new_list.append(float(user_more_questions.answer_5))
        new_list.append(float(user_more_questions.answer_6))

        product_id = request.data['data'][0]

        product_score = list(ProductScore.objects.filter(user_id=request.user.id).values())
        for o1 in product_score:
            product1 = Product.objects.get(pk=product_id)
            user_score_for_product = o1['score']
        print(user_score_for_product)
        print(new_list[0])
        new_cluster_taste = list()

        features = np.zeros((100, 5, 3))

        cls = list(Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                              'style_param_5'))

        clothes = [item for item in cls]
        for i in range(100):
            lst = list(clothes[i].values())
            for j in range(5):
                val = [int(x) for x in lst[j].split(',')]
                for k in range(3):
                    features[i][j][k] = val[k]

        rec_system = ai_similarity.RecommendationSystem(features)
        new_cluster_taste = rec_system.update_cluster_taste(new_list, user_score_for_product, product_id)

        new_cluster_taste = CreateRecSystem.rec_system.update_cluster_taste(new_list, user_score_for_product,
                                                                            product_id)
        p_data = {}
        # p_data['user_id'] = request.user.id
        p_data['answer_1'] = str(new_cluster_taste[0])
        p_data['answer_2'] = str(new_cluster_taste[1])
        p_data['answer_3'] = str(new_cluster_taste[2])
        p_data['answer_4'] = str(new_cluster_taste[3])
        p_data['answer_5'] = str(new_cluster_taste[4])
        p_data['answer_6'] = str(new_cluster_taste[5])

        print(p_data)

        data2 = {}
        user_more_questions.answer_1 = p_data['answer_1']
        user_more_questions.answer_2 = p_data['answer_2']
        user_more_questions.answer_3 = p_data['answer_3']
        user_more_questions.answer_4 = p_data['answer_4']
        user_more_questions.answer_5 = p_data['answer_5']
        user_more_questions.answer_6 = p_data['answer_6']
        user_more_questions.save()
        return Response(p_data, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self , request):
        mail_subject = 'reset password'
        message = 'newpass1234'
        to_email = request.data['email']
        print(to_email)
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        data2 ={"message" : "رمز جدید به ایمیل شما ارسال شد"}
        return Response(status=status.HTTP_200_OK , data = data2)
