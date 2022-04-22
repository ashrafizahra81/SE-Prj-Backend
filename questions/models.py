from django.db import models


class Answer(models.Model):
    answer_text = models.CharField(max_length=150)

    def __str__(self):
        return self.answer_text


class Question(models.Model):
    question_text = models.CharField(max_length=150)
    answer = models.OneToOneField('Answer', on_delete=models.CASCADE,
                                  related_name='correct_answer', null=True, blank=True)
    choices = models.ManyToManyField(Answer, related_name='choices')

    def __str__(self):
        return self.question_text
