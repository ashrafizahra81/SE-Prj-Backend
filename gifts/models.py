from django.db import models

# Create your models here.

class Gift(models.Model):
    type = models.CharField(max_length=20)
    discount_code = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    date = models.DateField(null = True) 
