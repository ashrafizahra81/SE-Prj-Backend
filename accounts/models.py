from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user_phone_number = models.CharField(max_length=20)
    user_postal_code = models.CharField(max_length=20)
    user_address = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
