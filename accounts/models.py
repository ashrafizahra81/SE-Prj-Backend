from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user_phone_number = models.CharField(max_length=20)
    user_postal_code = models.CharField(max_length=20)
    user_address = models.CharField(max_length=20)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


class Style(models.Model):
    style_description = models.CharField(max_length=1000, null=True)
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


class Shop(models.Model):
    shop_name = models.CharField(max_length=1000, null=False)
    shop_description = models.CharField(max_length=5000, null=True)
    shop_address = models.CharField(max_length=2000, null=True)
    shop_phone_num = models.IntegerField(null=True)
    shop_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False)
    product_description = models.CharField(max_length=2000, null=True)
    product_brand = models.CharField(max_length=100, null=True)
    product_color = models.CharField(max_length=100, null=False)
    product_size = models.CharField(max_length=100, null=False)
    product_price = models.BigIntegerField(null=False)
    product_off_percent = models.IntegerField(null=False, default=0)
    product_image = models.URLField(null=True)
    style_id = models.ForeignKey(Style, on_delete=models.DO_NOTHING)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    shop_id = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
