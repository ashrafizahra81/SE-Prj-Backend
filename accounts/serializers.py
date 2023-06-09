from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, UntypedToken

from Backend import settings
from .models import *

import django.contrib.auth.password_validation as validators
from rest_framework import generics
from wallets.models import Wallet
import logging

logger = logging.getLogger("django")
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
        fields = ('email', 'username', 'user_phone_number', 'user_postal_code', 'user_address')


# class StyleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Style
#         fields = ['style_image_url']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        logger.info('request recieved from POST /accounts/api/token/')
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        logger.info('Data entered is valid')
        if self.user.shop_name == None:
            logger.info('The user entered is a customer')
            data.update({'type': 'user'})
            data.update({'username': self.user.username})
            data.update({'email':self.user.email})
            data.update({'user_phone_number': self.user.user_phone_number})
            wallet = Wallet.objects.get(user = self.user)
            data.update({'balance': wallet.balance})
            data.update({'score': self.user.score})
        else:
            logger.info('The user entered is a seller')
            data.update({'type': 'seller'})
            data.update({'shop_name': self.user.shop_name})
            data.update({'email':self.user.email})
            data.update({'shop_phone_number': self.user.shop_phone_number})
        logger.info('The user logged in successfuly')
        return data


# class ProductsSerializer(serializers.ModelSerializer):

#     def validate(self, data):
#         return data

#     def create(self, validated_data):
#         shop = validated_data.get('shop', None)
#         product = Product.objects.create(**validated_data)
#         return product

#     class Meta:
#         model = Product
#         fields = '__all__'


# class ProductInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'upload']


# class EditProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         exclude = ('shop', 'upload')


class ShopManagerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'shop_name', 'shop_address',
                  'shop_phone_number')
        extera_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EditShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'user_phone_number', 'shop_name', 'shop_address',
            'shop_phone_number')


# class ProductAndStyleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAndStyle
#         exclude = ['shop_id', 'product', 'product_off_percent', 'style_param_1','style_param_2'
#                    ,'style_param_3','style_param_4','style_param_5','upload']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    serializers.ListField


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token).blacklist()
#         except TokenError:
#             self.fail('bad token')


# class MoreQuestionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductScore
#         fields = '__all__'


# class EditMoreQuestionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'



class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        logger.info('request recieved from POST /accounts/token/verify/')
        data = super(CustomTokenVerifySerializer, self).validate(attrs)
        logger.info('The token entered is valid')
        print(self)
        data.update({"status":"ok"})
        return data

class ShowShopManagerInfoSerializer(serializers.ModelSerializer):

     class Meta:
        model = User
        fields = (
            'email', 'username', 'user_phone_number', 'shop_name', 'shop_address',
            'shop_phone_number')
