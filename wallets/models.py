from django.db import models
from accounts.models import User
# Create your models here.

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    balance = models.FloatField(default=0, null=True)
