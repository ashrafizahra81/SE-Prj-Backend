from django.db import models
from accounts.models import User


class ListOfQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Questions')


class Question(models.Model):
    answer = models.IntegerField()
    question_id = models.IntegerField()
    questions = models.ForeignKey(ListOfQuestion, related_name='question', on_delete=models.CASCADE , null=True)
