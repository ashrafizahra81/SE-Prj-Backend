from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.

class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, null=True, default="not Accepted")

