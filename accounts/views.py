from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer


class UserRegister(APIView):
    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.POST)
        if serialized_data.is_valid():
            serialized_data.create(serialized_data.validated_data)
            return Response(serialized_data.data)
        return Response(serialized_data.errors)
