from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.


class UserFavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

