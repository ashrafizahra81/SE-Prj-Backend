from django.db import models

# Create your models here.


class User(models.Model):

    USER_EMAIL = models.EmailField(max_length=100)
    USER_PASSWORD = models.CharField(max_length=100)
    USER_NAME = models.CharField(max_length=1000)
    USER_PHONE_NUM = models.IntegerField()
    USER_POSTAL_CODE = models.IntegerField()
    USER_ADDRESS = models.CharField(max_length=100)
    
