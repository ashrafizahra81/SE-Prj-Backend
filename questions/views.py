from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserQuestionsSerializer
from accounts.serializers import StyleSerializer, ProductsSerializer, ProductInfoSerializer
from rest_framework.response import Response
from .models import UserQuestions, UserMoreQuestions
from accounts.models import Style, UserStyle, Product, ConstantStyles
from .ai_similarity import RecommendationSystem
import numpy as np
from rest_framework.permissions import IsAuthenticated
from accounts.views import CreateRecSystem


# Create your views here.
class UserQuestionView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        features = np.zeros((100, 5, 3))

        cls = list(Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                              'style_param_5'))

        clothes = [item for item in cls]
        for i in range(100):
            lst = list(clothes[i].values())
            for j in range(5):
                val = [int(x) for x in lst[j].split(',')]
                for k in range(3):
                    features[i][j][k] = val[k]

        s = UserQuestions(user_id=request.user.id,
                          answer_1=request.data['data'][0],
                          answer_2=request.data['data'][1],
                          answer_3=request.data['data'][2],
                          answer_4=request.data['data'][3],
                          answer_5=request.data['data'][4],
                          answer_6=request.data['data'][5],
                          answer_7=request.data['data'][6])
        s.save()
        first_feature = np.array([int(s.answer_1), int(s.answer_2), int(s.answer_3), int(s.answer_4), int(s.answer_5)])
        values = np.array([1, 1, 0, 0, 0])

        answer_6_list = [int(x) for x in s.answer_6.split(',')]
        answer_7_list = [int(x) for x in s.answer_7.split(',')]

        values[answer_6_list[0] + 1] = 0.8
        values[answer_6_list[1] + 1] = 0.6
        values[answer_6_list[2] + 1] = 0.4

        image1 = ConstantStyles.objects.get(id=answer_7_list[0])
        image2 = ConstantStyles.objects.get(id=answer_7_list[1])
        image3 = ConstantStyles.objects.get(id=answer_7_list[2])

        second_feature = np.array(
            [int(image1.style_param_1[0:1]), int(image1.style_param_2[0:1]), int(image1.style_param_3[0:1]),
             int(image1.style_param_4[0:1]),
             int(image1.style_param_5[0:1])])
        third_feature = np.array(
            [int(image2.style_param_1[0:1]), int(image2.style_param_2[0:1]), int(image2.style_param_3[0:1]),
             int(image2.style_param_4[0:1]),
             int(image2.style_param_5[0:1])])
        fourth_feature = np.array(
            [int(image3.style_param_1[0:1]), int(image3.style_param_2[0:1]), int(image3.style_param_3[0:1]),
             int(image3.style_param_4[0:1]),
             int(image3.style_param_5[0:1])])

        print(features)
        print(values)
        print(first_feature)
        print(second_feature)
        print(third_feature)
        print(fourth_feature)

        simil = RecommendationSystem(features)
        val = simil.recommend_based_on_questions(values, first_feature, second_feature, third_feature, fourth_feature)
        val = val + 1

        for st in val:
            us = UserStyle(user_id_id=request.user.id, style_id_id=st)
            us.save()

        a = Style.objects.filter(pk__in=list(val)).values('style_image_url')
        resp = StyleSerializer(instance=a, many=True)

        return Response(data=resp.data, status=status.HTTP_201_CREATED)


class SimilarClothesView(APIView):

    def get(self, request, pk):

        clothes_features = np.zeros((100, 5, 3))

        all_cls = list(Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                                  'style_param_5'))

        all_clothes = [item for item in all_cls]
        for i in range(100):
            lst = list(all_clothes[i].values())
            for j in range(5):
                resp = [int(x) for x in lst[j].split(',')]
                for k in range(3):
                    clothes_features[i][j][k] = resp[k]

        features = np.zeros((5, 3))

        cls = Style.objects.get(pk=pk)

        lst = [cls.style_param_1, cls.style_param_2, cls.style_param_3, cls.style_param_4, cls.style_param_5]

        for i in range(5):
            resp = [int(x) for x in lst[i].split(',')]
            for j in range(3):
                features[i][j] = resp[j]

        # rec_system = CreateRecSystem.rec_system
        rec_system = RecommendationSystem(clothes_features)
        resp = rec_system.recommend_based_on_clothes(selectedClothes=features, values=[1, 1, 1, 1, 1], anomaly=20)
        resp = resp + 1
        val = list(resp)

        a = Style.objects.filter(pk__in=val).values()
        products = []
        index = 1
        for i in list(a):
            if i['product_id']:
                product = Product.objects.get(pk=i['product_id'])
                ser = ProductsSerializer(instance=product).data
                ser['upload'] = i['style_image_url']
                ser['id'] = index
                products.append(ser)
            else:
                products.append({'id': index, 'upload': i['style_image_url']})
        index += 1

        return Response(data=products, status=status.HTTP_200_OK)


class MoreQuestionsView(APIView):
    def post(self, request):

        answered = UserMoreQuestions.objects.filter(user_id=request.user.id).exists()
        if answered:
            user_questions = UserMoreQuestions.objects.filter(user_id=request.user.id).values('answer_1', 'answer_2',
                                                                                              'answer_3', 'answer_4',
                                                                                              'answer_5', 'answer_6')

        else:
            if request.data:
                s = UserMoreQuestions(user_id=request.user.id,
                                      answer_1=request.data[0]['option'],
                                      answer_2=request.data[1]['option'],
                                      answer_3=request.data[2]['option'],
                                      answer_4=request.data[3]['option'],
                                      answer_5=request.data[4]['option'],
                                      answer_6=request.data[5]['option'])
                s.save()
                user_questions = UserMoreQuestions.objects.filter(user_id=request.user.id).values('answer_1',
                                                                                                  'answer_2',
                                                                                                  'answer_3',
                                                                                                  'answer_4',
                                                                                                  'answer_5',
                                                                                                  'answer_6')
            else:
                user_questions = ['2.5', '2.5', '2.5', '2.5', '2.5', '2.5']


        features = np.zeros((100, 5, 3))

        cls = list(Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                              'style_param_5'))

        clothes = [item for item in cls]
        for i in range(100):
            lst = list(clothes[i].values())
            for j in range(5):
                val = [int(x) for x in lst[j].split(',')]
                for k in range(3):
                    features[i][j][k] = val[k]

        # rec_system = CreateRecSystem.rec_system
        rec_system = RecommendationSystem(features)

        cluster = [float(x) for x in user_questions]
        ret_val = rec_system.recommend_based_on_cluster(cluster)

        a = Style.objects.filter(pk__in=ret_val).values()
        products = []
        index = 1
        for i in list(a):
            if i['product_id']:
                product = Product.objects.get(pk=i['product_id'])
                ser = ProductsSerializer(instance=product).data
                ser['upload'] = i['style_image_url']
                ser['id'] = index
                products.append(ser)
            else:
                products.append({'id': index, 'upload': i['style_image_url']})
            index += 1

        return Response(data=products, status=status.HTTP_200_OK)


class NormalView(APIView):
    def get(self, pk):
        features = np.zeros((100, 5, 3))

        cls = list(Style.objects.all().values('style_param_1', 'style_param_2', 'style_param_3', 'style_param_4',
                                              'style_param_5'))

        clothes = [item for item in cls]
        for i in range(100):
            lst = list(clothes[i].values())
            for j in range(5):
                val = [int(x) for x in lst[j].split(',')]
                for k in range(3):
                    features[i][j][k] = val[k]

        rec_system = RecommendationSystem(clothes)

        ret_val = rec_system.normal_recommend_question2()
        for i in range(len(ret_val)):
            ret_val[i] += 1

        a = Style.objects.filter(pk__in=ret_val).values()
        products = []
        index = 1
        for i in list(a):
            if i['product_id']:
                product = Product.objects.get(pk=i['product_id'])
                ser = ProductsSerializer(instance=product).data
                ser['upload'] = i['style_image_url']
                ser['id'] = index
                products.append(ser)
            else:
                products.append({'id': index, 'upload': i['style_image_url']})
        index += 1

        print(products)

        return Response(data=products, status=status.HTTP_200_OK)
