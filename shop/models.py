from django.db import models


class Shop(models.Model):
    shop_name = models.CharField(max_length=1000, null=False)
    shop_description = models.CharField(max_length=5000, null=True)
    shop_address = models.CharField(max_length=2000, null=True)
    shop_phone_num = models.IntegerField(null=True)
    shop_owner_id = models.CharField(max_length=20)


class Product(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    image = models.URLField(null=True)
    shop_id = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=0)

class Category(models.Model):
    category_description = models.CharField(max_length=100, null=False)
