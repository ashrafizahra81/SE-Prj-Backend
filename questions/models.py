from django.db import models
from accounts.models import User


class UserQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    answer_1 = models.IntegerField(default=0)
    answer_2 = models.IntegerField(default=0)
    answer_3 = models.IntegerField(default=0)
    answer_4 = models.IntegerField(default=0)
    answer_5 = models.IntegerField(default=0)
    answer_6 = models.CharField(max_length=100, default='1,2,3')
    answer_7 = models.CharField(max_length=100, default='1,2,3')
