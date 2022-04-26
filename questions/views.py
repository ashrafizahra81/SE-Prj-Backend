from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserQuestionsSerializer
from rest_framework.response import Response
from .models import UserQuestions
from accounts.models import Style


# Create your views here.
class UserQuestionView(APIView):
    def post(self, request):
        print(request.data)
        s = UserQuestions(user_id=request.data['data'][0],
                          answer_1=request.data['data'][1],
                          answer_2=request.data['data'][2],
                          answer_3=request.data['data'][3],
                          answer_4=request.data['data'][4],
                          answer_5=request.data['data'][5],
                          answer_6_1=request.data['data'][6],
                          answer_6_2=request.data['data'][7],
                          answer_6_3=request.data['data'][8],
                          answer_7_1=request.data['data'][9],
                          answer_7_2=request.data['data'][10],
                          answer_7_3=request.data['data'][11])
        print(s)
        s.save()
        first_feature = [s.answer_1, s.answer_2, s.answer_3, s.answer_4, s.answer_5]
        second_feature = [0.8, 1, 0, 0, 0]

        second_feature[s.answer_6_1 + 1] = 0.8
        second_feature[s.answer_6_2 + 1] = 0.6
        second_feature[s.answer_6_3 + 1] = 0.4

        image1 = Style.objects.get(id=s.answer_7_1)
        image2 = Style.objects.get(id=s.answer_7_2)
        image3 = Style.objects.get(id=s.answer_7_3)
        thirdFeature = [image1.style_param_1, image1.style_param_2, image1.style_param_3, image1.style_param_4,
                        image1.style_param_5]
        forthFeature = [image2.style_param_1, image2.style_param_2, image2.style_param_3, image2.style_param_4,
                        image2.style_param_5]
        fifthFeature = [image3.style_param_1, image3.style_param_2, image3.style_param_3, image3.style_param_4,
                        image3.style_param_5]

        # print(thirdFeature)
        # print(forthFeature)
        # print(fifthFeature)

        return Response(status=status.HTTP_201_CREATED)
