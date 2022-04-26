from django.db import models
from accounts.models import User


class UserQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    answer_1 = models.IntegerField(default=0)
    answer_2 = models.IntegerField(default=0)
    answer_3 = models.IntegerField(default=0)
    answer_4 = models.IntegerField(default=0)
    answer_5 = models.IntegerField(default=0)
    answer_6_1 = models.IntegerField(default=0)
    answer_6_2 = models.IntegerField(default=0)
    answer_6_3 = models.IntegerField(default=0)
    answer_7_1 = models.IntegerField(default=0)
    answer_7_2 = models.IntegerField(default=0)
    answer_7_3 = models.IntegerField(default=0)
    count_1 = models.IntegerField(default=5)
    count_2 = models.IntegerField(default=2)
    count_3 = models.IntegerField(default=2)
    count_4 = models.IntegerField(default=2)
