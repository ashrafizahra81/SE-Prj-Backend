from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, related_name='orders')
    total_cost = models.IntegerField(default=0)
    off_cost = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    status = models.CharField(max_length=100, null=False)
    order_date = models.DateTimeField(auto_now_add=True, null=False)
    complete_date = models.DateTimeField(null=True)

