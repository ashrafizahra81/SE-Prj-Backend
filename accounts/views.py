from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from rest_framework.authtoken.models import Token

class UserRegister(APIView):
    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.POST)
        data = {}
        if serialized_data.is_valid():
            account = serialized_data.save()
            data['response'] = "successfully registered"
            data['email'] = account.email
            data['username'] = account.username
            data['user_phone_number'] = account.user_phone_number
            data['user_postal_code'] = account.user_postal_code
            data['user_address'] = account.user_address
            token = Token.objects.get(user = account).key
            data['token'] = token
            #serialized_data.create(serialized_data.validated_data)
            return Response(data)
        return Response(serialized_data.errors)
