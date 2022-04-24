from django.db import models
from accounts.models import User


class Question(models.Model):
    question_description = models.CharField(max_length=5000, null=False)
    question_answer = models.IntegerField(null=False)


class UserQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
