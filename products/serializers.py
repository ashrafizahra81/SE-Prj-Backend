from rest_framework import serializers
from Backend import settings
from .models import *
from shoppingCarts.models import UserShoppingCart
from favoriteProducts.models import UserFavoriteProduct
import logging
from datetime import datetime
logger = logging.getLogger("django")

class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('shop', 'upload')


class SaveProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['last_product_sold_date','number_of_votes','score','is_deleted','product_off_percent','upload']

class ProductsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = ['last_product_sold_date','number_of_votes','score','is_deleted','product_off_percent','upload','shop','is_available','initial_inventory']

class ProductAndStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['shop', 'product_off_percent','upload']

class ProductsOfOrderSerializer(serializers.ModelSerializer):
    upload = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name', 'product_size','product_color','product_price','inventory','upload','shop_id']
    def get_upload(self , obj):
        return obj['product_image']

class ShowProductsSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_is_favorite(self, obj):
        user_id = self.context.get("user_id")
        if(UserFavoriteProduct.objects.filter(user_id=user_id, product_id=obj.pk).exists()):
            logger.info('product with id '+str(obj.pk)+' is in favorite list')
            return True
        return False
    
    def get_is_in_cart(self, obj):
        user_id = self.context.get("user_id")
        if(UserShoppingCart.objects.filter(user_id=user_id, product_id=obj.pk).exists()):
            logger.info('product with id '+str(obj.pk)+' is in shopping cart')
            return True
        return False
    

class ProductOfShopSerializer(serializers.ModelSerializer):
        product_off_percent = serializers.SerializerMethodField()
        upload = serializers.SerializerMethodField()
        class Meta:
            model = Product
            fields = ['id','product_name','product_price','product_off_percent','upload','shop_id' , 'inventory']
        def get_product_off_percent(self , obj):
            price_off = 0
            if int(obj['product_off_percent']) > 0:
                    price_off = ((100 - int(obj['product_off_percent'])) / 100) * int(obj['product_price'])
            return price_off
        
        def get_upload(self , obj):
            return obj['product_image']
        
class ReportSerializer(serializers.ModelSerializer):
    totalPriceOfProduct = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    class Meta:
        model  = Product
        model_fields = ['product_name','inventory','initial_inventory','product_price','date']
        extra_fields = ['totalPriceOfProduct']
        fields = model_fields+extra_fields
    
    def get_totalPriceOfProduct(self , obj):
        return (obj['initial_inventory'] - obj['inventory']) * obj['product_price']
    
    def get_date(self , obj):

        if(obj['last_product_sold_date'] != None):
            return datetime.date(obj['last_product_sold_date'])
        else :
            return "تاکنون خریدی انجام نشده"
        

class FilterSerializer(serializers.ModelSerializer):
    upload = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','product_price','upload','shop_id']
    def get_upload(self , obj):
            return obj['product_image']

