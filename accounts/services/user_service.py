from .user_interface import UserService
from ..models import User
from django.contrib.auth.hashers import make_password
from accounts.serializers import *

class ConcreteUserService(UserService):
    def updateUser(self, data, is_valid):
        
        serialized_data = UserRegisterSerializer(data=data)
        if serialized_data.is_valid():
            account = serialized_data.save()
            account.is_active = is_valid
            account.save()

    def updateUserScore(self, score, email):
        user = User.objects.get(email=email)
        user.score += score
        user.save() 

    def updateUserIsValid(self, user, is_valid):
        user.is_active = is_valid
        user.save()
    
    def updateUserPassword(self, user, password):

        user.random_integer=None
        user.password = make_password(password)
        user.save()
    
    def updateUserCode(self, user, code):
        user.random_integer=code
        user.save()
        
        