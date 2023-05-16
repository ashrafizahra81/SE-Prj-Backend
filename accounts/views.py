from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .serializers import *
from .models import *
from rest_framework import status
from datetime import datetime
from datetime import datetime
import random
from wallets.models import Wallet
from rest_framework.decorators import api_view, permission_classes
from . import send_mail
from django.contrib.auth.hashers import make_password
from datetime import datetime
from permissions import IsShopOwner



def sendEmail(self , email):
    token=random.randint(1000,9999)
    to_emails = []
    to_emails.append(email)
    send_mail.send_mail(html=token,text='Here is the code ',subject='verification',from_email='',to_emails=to_emails)
    return token

class UserRegister(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.data)
        if(User.objects.filter(email=request.data['email']).exists()):
            userCode = CodesForUsers.objects.get(email = request.data['email'])
            now = datetime.now()
            delta = now - userCode.created_at.replace(tzinfo=None)
            diff = delta.seconds
            if(diff > 600):
                token = sendEmail(self , userCode.email)
                userCode.created_at = datetime.now()
                userCode.code = token
                userCode.save()
                return Response({"message":"کد جدید به ایمیل ارسال شد"},
                            status=status.HTTP_201_CREATED)
            return Response({"message":"کد به ایمیل شما ارسال شده است"},
                            status=status.HTTP_202_ACCEPTED)
        data = {}
        if serialized_data.is_valid():
            account = serialized_data.save()
            account.is_active = 0
            account.save()
            token = sendEmail(self , account.email)
            user_code = CodesForUsers(
                code = token,
                created_at = datetime.now(),
                email = account.email 
            )
            user_code.save()
            wallet = Wallet(
                user = account,
                balance = 0, 
            )
            wallet.save()
            return Response(data = data , status=status.HTTP_200_OK)
        return Response(serialized_data.errors)

class verfyUserToResgister(APIView):
    def post(self , request):
        if(not(request.data['code'] <=9999 and request.data['code'] >= 1000)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(CodesForUsers.objects.filter(code=request.data['code']).exists()):

            userCode = CodesForUsers.objects.get(code = request.data['code'])
            userCode.code=None
            userCode.save()
            user = User.objects.get(email = userCode.email)
            user.is_active = 1
            user.save()
            data={}
            if(user.shop_name == None):
                data['username'] = user.username
                data['email'] = user.email
                data['user_phone_number'] = user.user_phone_number
                data['balance'] = 0
                refresh = RefreshToken.for_user(user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                data['score'] = 0
            else:
                data['username'] = user.username
                data['email'] = user.email
                data['shop_name'] = user.shop_name
                data['shop_address'] = user.shop_address
                data['shop_phone_number'] = user.shop_phone_number
                refresh = RefreshToken.for_user(user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
            return Response(data=data , status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """

    serializer_class = CustomTokenVerifySerializer


class UserEditProfile(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserEditProfileSerializer
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        data1 = {}

        data1['email'] = user.email
        data1['username'] = user.username
        data1['user_phone_number'] = user.user_phone_number
        data1['user_postal_code'] = user.user_postal_code
        data1['user_address'] = user.user_address

        data = {}

        serialized_data = UserEditProfileSerializer(instance=user, data=request.data, partial=True)
        if serialized_data.is_valid():

            if(not(request.data['user_postal_code'].isdigit())):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if(not(request.data['user_phone_number'].isdigit())):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            edited_user = serialized_data.save()
            if data1['email'] != edited_user.email:
                data['email'] = edited_user.email
            else:
                data['email'] = ""

            if data1['username'] != edited_user.username:
                data['username'] = edited_user.username
            else:
                data['username'] = ""

            if data1['user_phone_number'] != edited_user.user_phone_number:
                data['user_phone_number'] = edited_user.user_phone_number
            else:
                data['user_phone_number'] = ""

            if data1['user_postal_code'] != edited_user.user_postal_code:
                data['user_postal_code'] = edited_user.user_postal_code
            else:
                data['user_postal_code'] = ""

            if data1['user_address'] != edited_user.user_address:
                data['user_address'] = edited_user.user_address
            else:
                data['user_address'] = ""

            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopManagerRegister(APIView):
    serializer_class = ShopManagerRegisterSerializer
    def post(self, request):
        serialized_data = ShopManagerRegisterSerializer(data=request.data)
        if(User.objects.filter(email=request.data['email']).exists()):
            userCode = CodesForUsers.objects.get(email = request.data['email'])
            now = datetime.now()
            delta = now - userCode.created_at.replace(tzinfo=None)
            diff = delta.seconds
            if(diff > 600):
                token = sendEmail(self , userCode.email)
                userCode.created_at = datetime.now()
                userCode.code = token
                userCode.save()
                return Response({"message":"کد جدید به ایمیل ارسال شد"},
                            status=status.HTTP_201_CREATED)
            return Response({"message":"کد به ایمیل شما ارسال شده است"},
                            status=status.HTTP_202_ACCEPTED)
        data = {}
        if serialized_data.is_valid():
            account = serialized_data.save()
            account.is_active = 0
            account.save()
            token = sendEmail(self , account.email)
            user_code = CodesForUsers(
                code = token,
                created_at = datetime.now(),
                email = account.email 
            )
            user_code.save()
            return Response(data)
        return Response(serialized_data.errors)


class EditShop(APIView):
    permission_classes = [IsShopOwner ,]
    serializer_class = EditShopSerializer
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        data1 = {}
        data1['username'] = user.username
        data1['user_phone_number'] = user.user_phone_number
        data1['email'] = user.email
        data1['shop_address'] = user.shop_address
        data1['shop_name'] = user.shop_name
        data1['shop_phone_number'] = user.shop_phone_number
        serialized_data = EditShopSerializer(data=request.data, instance=user, partial=True)
        data = {}
        if serialized_data.is_valid():
            if(not(request.data['shop_phone_number'].isdigit())):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if(not(request.data['user_phone_number'].isdigit())):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            edited_shop = serialized_data.save()

            if data1['username'] != edited_shop.username:
                data['username'] = edited_shop.username
            else:
                data['username'] = ""

            if data1['user_phone_number'] != edited_shop.user_phone_number:
                data['user_phone_number'] = edited_shop.user_phone_number
            else:
                data['user_phone_number'] = ""

            if data1['email'] != edited_shop.email:
                data['email'] = edited_shop.email
            else:
                data['email'] = ""

            if data1['shop_address'] != edited_shop.shop_address:
                data['shop_address'] = edited_shop.shop_address
            else:
                data['shop_address'] = ""

            if data1['shop_name'] != edited_shop.shop_name:
                data['shop_name'] = edited_shop.shop_name
            else:
                data['shop_name'] = ""

            if data1['shop_phone_number'] != edited_shop.shop_phone_number:
                data['shop_phone_number'] = edited_shop.shop_phone_number
            else:
                data['shop_phone_number'] = ""

            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
      
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowUserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        userObj = User.objects.get(id=request.user.id)
        data = {}
        if userObj.shop_name == None:
            data['email'] = userObj.email
            data['username'] = userObj.username
            data['user_phone_number'] = userObj.user_phone_number
            data['user_postal_code'] = userObj.user_postal_code
            data['user_address'] = userObj.user_address
            wallet = Wallet.objects.get(user = userObj)
            data['inventory'] = wallet.balance
        else:
            data['email'] = userObj.email
            data['username'] = userObj.username
            data['shop_name'] = userObj.shop_name
            data['shop_phone_number'] = userObj.shop_phone_number
            data['user_phone_number'] = userObj.user_phone_number
            data['shop_address'] = userObj.shop_address

        return Response(data, status=status.HTTP_200_OK)


class Logout(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class show_score(APIView):
     permission_classes = [IsAuthenticated, ]
     def get(self , request):
        data = {}
        data['score'] = request.user.score
        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reset_password(request):
    if request.method =='POST':
        data2 = request.data
        token_recieved=data2['token']
        password=data2['password']
        password_again=data2['password2']
        used = User.objects.get(id=request.user.id)
        if int(token_recieved) !=used.random_integer:
            return Response({'message':'Invalid Token'} , status=status.HTTP_400_BAD_REQUEST)

        if password!=password_again:
            return Response({'message':'Passwords should match'} , status=status.HTTP_400_BAD_REQUEST)
        used.random_integer=None
        used.password = make_password(password)
        used.save()
        return Response('Password changed successfully')
    token1=random.randint(1000,9999)
    used=User.objects.get(id=request.user.id)
    used.random_integer=token1
    used.save()
    to_emails = []
    to_emails.append(used.email)
    send_mail.send_mail(html=token1,text='Here is your password reset token',subject='password reset token',from_email='',to_emails=to_emails)
    return Response('working now')



class ReceiveEmailForRecoverPassword(APIView):
    def post(self, request):
        data = request.data
        email1 = data['email']
        user = CodesForUsers.objects.filter(email=email1).exists()
        print(user)
        print("model is ok")
        f = 0
        if user != False:
            user = CodesForUsers.objects.get(email=email1)
            now = datetime.now()
            print("userrr")
            print(user.id)
            print(type(user.created_at))
            delta = now - user.created_at.replace(tzinfo=None)
            print(now)
            print(user.created_at.replace(tzinfo=None))
            print("deltaaa")
            print(delta)
            diff = delta.seconds
            print("diiiiiff")
            print(diff)
            if diff > 600:
                token1=random.randint(1000,9999)
                user.code = token1
                user.created_at = datetime.now()
                print("newww")
                print(user.created_at)
                user.save()
        else:
            token1=random.randint(1000,9999)
            user = CodesForUsers(
                code = token1,
                created_at = datetime.now(),
                email= email1,
            )
            user.save()
        to_emails = []
        to_emails.append(user.email)
        send_mail.send_mail(html=user.code,text='Here is your password recovery token',subject='password recovery token',from_email='',to_emails=to_emails)
        data3 = {}
        data3['id'] = user.id
        
        
        return Response(data3, status=status.HTTP_200_OK)

class RecoverPassword(APIView):
    def post(self, request, pk):
        print("here in post 1")
        data2 = request.data
        print("here in post 2")
        token_recieved=data2['token']
        password=data2['password']
        password_again=data2['password2']
        user = CodesForUsers.objects.get(pk=pk)
        data3 = {}
        data3['code-id'] = user.id
        if token_recieved !=user.code:
            return Response({'message':'Invalid Token'} , status=status.HTTP_400_BAD_REQUEST)
        if password!=password_again:
            return Response({'message':'Passwords should match'} , status=status.HTTP_400_BAD_REQUEST)
        mainUser = User.objects.get(email=user.email)
        mainUser.password = make_password(password)
        mainUser.save()
        return Response({'message':'Password changed successfully'} , status=status.HTTP_200_OK)