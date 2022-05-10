from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from shop.models import Product


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=20)
    user_postal_code = models.CharField(max_length=20, null=True)
    user_address = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


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

class UserShoppingCart(models.Model):
    user = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product , on_delete=models.DO_NOTHING)
