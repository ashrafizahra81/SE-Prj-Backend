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
        # data1 = UserQuestions.objects.bulk_create()
        # print(data1)
        # for i in data1:
        #     i.save()
        for i in request.data:
            s = UserQuestions(question_id=i['question_id'], user_id=i['user_id'])
            print(s)
            s.save()
        return Response(status=status.HTTP_201_CREATED)
