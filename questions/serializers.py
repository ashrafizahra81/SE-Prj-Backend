from rest_framework import serializers
from .models import Question, ListOfQuestion


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_id', 'answer']


class ListOfQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True , read_only=True)

    class Meta:
        model = ListOfQuestion
        fields = ['question']
