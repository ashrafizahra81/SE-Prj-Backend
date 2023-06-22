from rest_framework import serializers
from Backend import settings
from .models import *
from shoppingCarts.models import UserShoppingCart
from favoriteProducts.models import UserFavoriteProduct
import logging
from datetime import datetime
logger = logging.getLogger("django")

class ShowFavoriteProductsSerializer(serializers.ModelSerializer):
        product_off_percent = serializers.SerializerMethodField()
        upload = serializers.SerializerMethodField()
        class Meta:
            model = Product
            fields = ['id','product_name','product_price','product_off_percent','upload','shop_id']
        def get_product_off_percent(self , obj):
            price_off = 0
            if int(obj['product_off_percent']) > 0:
                    price_off = ((100 - int(obj['product_off_percent'])) / 100) * int(obj['product_price'])
            return price_off
        
        def get_upload(self , obj):
            return obj['product_image']