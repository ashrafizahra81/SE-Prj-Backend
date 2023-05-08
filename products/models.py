from django.db import models
from accounts.models import User

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False)
    product_price = models.BigIntegerField(null=False)
    shop = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='products')
    upload = models.FileField(upload_to='uploads/', null=True)
    inventory = models.IntegerField(default=0, null=False)
    initial_inventory = models.IntegerField(default=0, null=False)
    product_size = models.CharField(max_length=100, null=True)
    product_group = models.CharField(max_length=100, null=True)
    product_image = models.CharField(max_length=2000, null=True)
    product_color = models.CharField(max_length=100, null=True)
    product_height = models.IntegerField(default=0)
    product_design = models.CharField(max_length=100, null=True)
    product_material = models.CharField(max_length=100, null=True)
    product_country = models.CharField(max_length=100, null=True)
    product_off_percent = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    score = models.FloatField(default=0, null=True)
    number_of_votes = models.IntegerField(default=0, null=True)
    last_product_sold_date = models.DateTimeField(null = True)