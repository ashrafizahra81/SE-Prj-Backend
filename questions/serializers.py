from rest_framework import serializers
from .models import UserQuestions


class UserQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestions
        fields = ['id', 'user']
