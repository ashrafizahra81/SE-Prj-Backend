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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
