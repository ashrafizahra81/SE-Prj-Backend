from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserQuestionsSerializer
from accounts.serializers import StyleSerializer
from rest_framework.response import Response
from .models import UserQuestions
from accounts.models import Style, UserStyle
from .ai_similarity import Similarity
import numpy as np


# Create your views here.
class UserQuestionView(APIView):

    def post(self, request):

        features = np.zeros((100, 5))

        cls = Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                         'style_param_5')

        clothes = [item for item in cls]
        for i in range(100):
            lst = list(clothes[i].values())
            for j in range(5):
                features[i][j] = lst[j]

        s = UserQuestions(user_id=request.data['data'][0],
                          answer_1=request.data['data'][1],
                          answer_2=request.data['data'][2],
                          answer_3=request.data['data'][3],
                          answer_4=request.data['data'][4],
                          answer_5=request.data['data'][5],
                          answer_6=request.data['data'][6],
                          answer_7=request.data['data'][7])
        s.save()
        first_feature = np.array([s.answer_1, s.answer_2, s.answer_3, s.answer_4, s.answer_5])
        values = np.array([0.8, 1, 0, 0, 0])

        answer_6_list = [int(x) for x in s.answer_6.split(',')]
        answer_7_list = [int(x) for x in s.answer_7.split(',')]

        values[answer_6_list[0] + 1] = 0.8
        values[answer_6_list[1] + 1] = 0.6
        values[answer_6_list[2] + 1] = 0.4

        image1 = Style.objects.get(id=answer_7_list[0])
        image2 = Style.objects.get(id=answer_7_list[1])
        image3 = Style.objects.get(id=answer_7_list[2])

        second_feature = np.array(
            [image1.style_param_1, image1.style_param_2, image1.style_param_3, image1.style_param_4,
             image1.style_param_5])
        third_feature = np.array(
            [image2.style_param_1, image2.style_param_2, image2.style_param_3, image2.style_param_4,
             image2.style_param_5])
        fourth_feature = np.array(
            [image3.style_param_1, image3.style_param_2, image3.style_param_3, image3.style_param_4,
             image3.style_param_5])

        simil = Similarity(features)
        val = simil.recommend(values, first_feature, second_feature, third_feature, fourth_feature)
        val = val + 1

        for st in val:
            us = UserStyle(user_id_id=s.user_id, style_id_id=st)
            us.save()

        a = Style.objects.filter(pk__in=list(val)).values('style_image_url')
        resp = StyleSerializer(instance=a, many=True)

        return Response(data=resp.data, status=status.HTTP_201_CREATED)
