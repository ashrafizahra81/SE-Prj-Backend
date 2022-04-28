from rest_framework import serializers
from .models import UserQuestions


class UserQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestions
        fields = ['user', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5', 'answer_6', 'answer_7']
