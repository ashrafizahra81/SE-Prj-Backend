from django.shortcuts import render
from accounts.models import User
from shoppingCarts.models import UserShoppingCart
from favoriteProducts.models import UserFavoriteProduct
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from permissions import IsShopOwner
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
# Create your views here.



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
    permission_classes = [IsAuthenticated, IsShopOwner]

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        self.check_object_permissions(request, product)
        product.is_deleted = True
        product.save()
        # product.delete()
        return Response({'message': 'محصول موردنظر با موفقیت حذف شد'})


class GetProductInfo(APIView):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        score = 0
        user_score_for_product = 0
        ret_val = {}
        if product and product.is_deleted == False:
            serialized_data = ProductsSerializer(instance=product, data=request.data, partial=True)
            if serialized_data.is_valid():
                ret_val = serialized_data.data
                is_fav = UserFavoriteProduct.objects.filter(user_id=request.user.id, product_id=product.pk).exists()
                in_cart = UserShoppingCart.objects.filter(user_id=request.user.id, product_id=product.pk).exists()
                ret_val['is_favorite'] = is_fav
                ret_val['is_in_cart'] = in_cart
                # product_score = list(ProductScore.objects.filter(user_id=request.user.id).values())
                # for o1 in product_score:
                #     # product1 = Product.objects.get(pk=product_id)
                #     if o1['product_id'] == pk:
                #         user_score_for_product = o1['score']
                score = user_score_for_product
                ret_val['score'] = score
                return Response(ret_val, status=status.HTTP_200_OK)
            else:
                return Response(serialized_data.errors, status=status.HTTP_417_EXPECTATION_FAILED)

        return Response(status=status.HTTP_204_NO_CONTENT)


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
                initial_inventory = data2['inventory'],
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
            # s = Style(product=product,
            #           style_image_url=data1['product_image'],
            #           style_param_1=data2['style_param_1'],
            #           style_param_2=data2['style_param_2'],
            #           style_param_3=data2['style_param_3'],
            #           style_param_4=data2['style_param_4'],
            #           style_param_5=data2['style_param_5']
            #           )
            # s.save()
            return Response(data=data1, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # NOQA


class ShowProductsByShop(APIView):

    def get(self, request):
        product_list = list(Product.objects.filter(shop=request.user.id).values())
        shop = User.objects.filter(id=request.user.id).values()
        print(shop)
        data = {}
        data1 = list()
        for i in product_list:
            data = {}
            if i['is_deleted'] == False:
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
            if len(data) != 0:
                data1.append(data)
        data2 = {}
        data2["products"] = data1
        data2["shop_name"] = shop[0]['shop_name']
        data2["shop_address"] = shop[0]['shop_address']
        data2["shop_phone_number"] = shop[0]['shop_phone_number']
        return Response(data2, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)


class ShowAllProducts(APIView):
    def get(self, request):
        product_list = list(Product.objects.all().values())
        data = {}
        data1 = list()
        print(product_list)
        for i in product_list:
            data = {}
            if i['is_deleted'] == False:

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
            if len(data) != 0:
                data1.append(data)
        return Response(data1, status=status.HTTP_200_OK)



class Report(APIView):

    permission_classes = [IsAuthenticated, ]
    
    def get(self , request):
        data = list()
        totalPriceOfShop = 0
        for product in Product.objects.all():
            data1={}
            if product.shop_id == request.user.id:
                totalPrice = (product.initial_inventory - product.inventory) * product.product_price
                totalPriceOfShop += totalPrice
                data1['productName'] = product.product_name
                data1['inventory'] = product.inventory
                data1['initial_inventory'] = product.initial_inventory
                data1['price'] = product.product_price
                data1['totalPriceOfProduct'] = totalPrice
                if(product.last_product_sold_date != None):
                    data1['date'] = datetime.date(product.last_product_sold_date)
                else :
                    data1['date'] = "تاکنون خریدی انجام نشده"
                data.append(data1)
        data.append({'totalSell':totalPriceOfShop})
        return Response(data, status=status.HTTP_200_OK)


class Filters(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        filter = request.data['group'][0]

        data1 = list()
        if filter == "شلوار" or filter == "پیراهن" or filter == "تیشرت" or filter == "هودی":
            products = list(Product.objects.filter(product_group=filter).values())
            for p in products:
                data = {}
                if p['is_deleted'] == False:
                    data['id'] = p['id']
                    # print(product.pk)
                    data['product_name'] = p['product_name']
                    # data['product_size'] = product['product_size']
                    # data['product_color'] = product['product_color']
                    data['product_price'] = p['product_price']
                    price_off = 0
                    # if p[0]['product_off_percent'] > 0:
                    #     price_off = ((100 - p[0]['product_off_percent']) / 100) * p[0]['product_price']
                    # data['product_off_percent'] = price_off
                    # data['inventory'] = i['inventory']
                    if p['upload']:
                        data['upload'] = p['upload']
                    else:
                        data['upload'] = p['product_image']
                    data['shop_id'] = p['shop_id']
                    data1.append(data)
        return Response(data1, status=status.HTTP_200_OK)