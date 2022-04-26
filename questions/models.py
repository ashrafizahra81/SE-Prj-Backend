from django.db import models
from accounts.models import User


class Question(models.Model):
    question_description = models.CharField(max_length=5000, null=False)
    #value = models.FloatField(default=0)


class UserQuestions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, default=1)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    answer_1 = models.IntegerField(default=0)
    answer_2 = models.IntegerField(default=0)
    answer_3 = models.IntegerField(default=0)
    answer_4 = models.IntegerField(default=0)
    answer_5 = models.IntegerField(default=0)
    answer_6 = models.CharField(max_length=100, default='')
    answer_7 = models.CharField(max_length=100, default='')
