from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import QuestionSerializer, UserQuestionsSerializer
from rest_framework.response import Response
from .models import UserQuestions , Question
from accounts.models import Style


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

        secondFeature = [0.8, 1, 0, 0, 0]

        for i in range(3):
            if list_answer6[i] == '1':
                secondFeature[i+2] = 0.8
            if list_answer6[i] == '2':
                secondFeature[i + 2] = 0.6
            if list_answer6[i] == '3':
                secondFeature[i + 2] = 0.4

        # print(secondFeature)

        list_answer7 = s.answer_7.split(",")
        image1 = Style.objects.get(id=list_answer7[0])
        image2 = Style.objects.get(id=list_answer7[1])
        image3 = Style.objects.get(id=list_answer7[2])
        thirdFeature = [image1.style_param_1, image1.style_param_2, image1.style_param_3, image1.style_param_4, image1.style_param_5]
        forthFeature = [image2.style_param_1, image2.style_param_2, image2.style_param_3, image2.style_param_4, image2.style_param_5]
        fifthFeature = [image3.style_param_1, image3.style_param_2, image3.style_param_3, image3.style_param_4, image3.style_param_5]

        # print(thirdFeature)
        # print(forthFeature)
        # print(fifthFeature)

        return Response(status=status.HTTP_201_CREATED)
