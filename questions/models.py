from django.db import models
from accounts.models import User


class UserQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    answer_1 = models.CharField(max_length=100, default='')
    answer_2 = models.CharField(max_length=100, default='')
    answer_3 = models.CharField(max_length=100, default='')
    answer_4 = models.CharField(max_length=100, default='')
    answer_5 = models.CharField(max_length=100, default='')
    answer_6 = models.CharField(max_length=100, default='1,2,3')
    answer_7 = models.CharField(max_length=100, default='1,2,3')


class UserMoreQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    answer_1 = models.CharField(max_length=100, default='2.5')
    answer_2 = models.CharField(max_length=100, default='2.5')
    answer_3 = models.CharField(max_length=100, default='2.5')
    answer_4 = models.CharField(max_length=100, default='2.5')
    answer_5 = models.CharField(max_length=100, default='2.5')
    answer_6 = models.CharField(max_length=100, default='2.5')
