from rest_framework import serializers
from Backend import settings
from .models import *


class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('shop', 'upload')


class ProductsSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return data

    # def create(self, validated_data):
    #     shop = validated_data.get('shop', None)
    #     product = Product.objects.create(**validated_data)
    #     return product

    class Meta:
        model = Product
        fields = '__all__'


class ProductAndStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['shop', 'product_off_percent','upload']

class ProductsOfOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_size','product_color','product_price','inventory','upload','shop_id']