from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=20, null=True)
    user_postal_code = models.CharField(max_length=20, null=True)
    user_address = models.CharField(max_length=20, null=True)
    shop_name = models.CharField(max_length=1000, null=True)
    shop_description = models.CharField(max_length=5000, null=True)
    shop_address = models.CharField(max_length=2000, null=True)
    shop_phone_number = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


# class Shop(models.Model):
#
#     shop_name = models.CharField(max_length=1000, null=False)
#     shop_description = models.CharField(max_length=5000, null=True)
#     shop_address = models.CharField(max_length=2000, null=True)
#     shop_phone_num = models.IntegerField(null=True)
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='shop')


class Style(models.Model):
    style_image_url = models.URLField(null=True)
    style_param_1 = models.IntegerField(default=0)
    style_param_2 = models.IntegerField(default=0)
    style_param_3 = models.IntegerField(default=0)
    style_param_4 = models.IntegerField(default=0)
    style_param_5 = models.IntegerField(default=0)


class UserStyle(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    style_id = models.ForeignKey(Style, on_delete=models.DO_NOTHING)


class Category(models.Model):
    category_description = models.CharField(max_length=100, null=False)

class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False)
    product_description = models.CharField(max_length=2000, null=True)
    product_price = models.BigIntegerField(null=False)
    shop_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='products')
    upload = models.FileField(upload_to='uploads/', null=True)
    # product_brand = models.CharField(max_length=100, null=True)
    # product_color = models.CharField(max_length=100, null=False)
    # product_size = models.CharField(max_length=100, null=False)
    # product_off_percent = models.IntegerField(null=False, default=0)
    # style_id = models.ForeignKey(Style, on_delete=models.DO_NOTHING, null = True)
    # category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null = True)
    # product_image = models.URLField(null=True)
    # file will be saved to MEDIA_ROOT / uploads / 2015 / 01 / 30
    # upload = models.FileField(upload_to='uploads/% Y/% m/% d/')



class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, null=True, default="not Accepted")



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, related_name='orders')
    cost = models.IntegerField()
    status = models.CharField(max_length=100, default="Accepted", null=False)
    order_date = models.DateTimeField(auto_now_add=True, null=False)
    complete_date = models.DateTimeField(null=True)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token
# (sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
