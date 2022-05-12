from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_phone_number', 'password')
        extera_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'user_phone_number')

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['style_image_url']


# class ShopSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = ('id', 'shop_name', 'shop_description', 'shop_address', 'shop_phone_num')
#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        # data.clear()
        # data.update({'email': self.user.email})
        # and everything else you want to send in the response
        return data

#####################################sprint3###########################################33
class ProductsSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return data

    def create(self, validated_data):
        shop = validated_data.get('shop', None)
        product = Product.objects.create(**validated_data)
        return product

    class Meta:
        model = Product
        exclude = ('shop',)

class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('product_image')

class ShopManagerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_phone_number', 'password', 'shop_name', 'shop_description', 'shop_address', 'shop_phone_num')
        extera_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EditShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'user_phone_number', 'shop_name', 'shop_description', 'shop_address', 'shop_phone_num')








#
# class ShopManagerRegistrationAndCreateShopSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Shop
#         #exclude = ('shop_owner', )
#         fields = ('username', 'email', 'user_phone_number', 'password', 'shop_name', 'shop_description', 'shop_address','shop_phone_num')
#         extera_kwargs = {
#             'password': {'write_only': True}
#         }
#
#         def create(self, validated_data):
#             return Shop.objects.create_shop(**validated_data)
#




# class CreateShopSerializer(serializers.ModelSerializer):
#     def validate(self, data):
#         return data
#
#     def create(self, validated_data):
#         shop_owner = validated_data.get('user', None)
#         shop = Shop.objects.create(**validated_data)
#         return shop
#
#     class Meta:
#         model = Shop
#         exclude = ('user', )







