from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import UserRegisterSerializer

class UserRegister(APIView):
    def get(self, request):
        return Response({'name' : 'zahra'})

