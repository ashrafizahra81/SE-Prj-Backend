from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import QuestionSerializer, UserQuestionsSerializer
from rest_framework.response import Response
from .models import UserQuestions , Question


# Create your views here.
class QuestionView(APIView):
    def post(self, request):
        print(request.data)
        for i in request.data:
            s = UserQuestions(user_id=i['user_id'], answer_1=i['answer_2'],
                              answer_2=i['answer_2'], answer_3=i['answer_3'], answer_4=i['answer_4'],
                              answer_5=i['answer_5'], answer_6=i['answer_6'], answer_7=i['answer_7'])
            print(s)
            s.save()
        firstFeature = [s.answer_1 , s.answer_2, s.answer_3, s.answer_4, s.answer_5]
        list_answer6 = s.answer_6.split(",")
        #print(list_answer6)
        qs = Question.objects.all()
        value1
        print(qs)
        secondFeature = [0.8 , 1 , ]
        return Response(status=status.HTTP_201_CREATED)
