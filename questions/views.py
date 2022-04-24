from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import QuestionSerializer, UserQuestionsSerializer
from rest_framework.response import Response
from .models import UserQuestions


# Create your views here.
class QuestionView(APIView):
    def post(self, request):
        print(request.data)
        for i in request.data:
            s = UserQuestions(user_id=i['user_id'], question_id=i['question_id'], answer_1=i['answer_2'],
                              answer_2=i['answer_2'], answer_3=i['answer_3'], answer_4=i['answer_4'],
                              answer_5=i['answer_5'], answer_6=i['answer_6'], answer_7=i['answer_7'])
            print(s)
            s.save()
        return Response(status=status.HTTP_201_CREATED)
