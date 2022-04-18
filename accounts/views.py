#from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import models
from .serializers import UserRegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

@api_view(['POST',])
def userRegister(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Registered successfully"
            data ['email'] = user.email
            data ['USER_NAME'] = user.USER_NAME
            data ['USER_PHONE_NUM'] = user.USER_PHONE_NUM
            data ['USER_POSTAL_CODE'] = user.USER_POSTAL_CODE
            data ['USER_ADDRESS'] = user.USER_ADDRESS
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            date = serializer.errors
        return Response(data)

