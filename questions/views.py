from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import QuestionSerializer, ListOfQuestionSerializer
from rest_framework.response import Response
from .models import ListOfQuestion


# Create your views here.
class QuestionView(APIView):
    def post(self,request):
        data1=ListOfQuestion.objects.bulk_create(request.POST)
        for i in data1 :
            i.save()
        data = ListOfQuestion.save(request.POST)
        print(data)
        ser_data = ListOfQuestionSerializer(data=request.POST , many=True , instance=data)
        if ser_data.is_valid():
            return Response(ser_data.data)
        return Response(ser_data.errors)

