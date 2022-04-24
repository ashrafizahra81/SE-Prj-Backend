from rest_framework import serializers
from .models import Question, UserQuestions


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_description' 'question_answer']


class UserQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestions
        fields = ['id', 'user', 'question']
