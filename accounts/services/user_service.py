from .user_interface import UserService
from ..models import User

class ConcreteUserService(UserService):
    def updateUser(self, serialized_data, is_valid):
        
        account = serialized_data.save()
        account.is_active = is_valid
        account.save()

    def updateUserScore(self, score, email):
        user = User.objects.get(email=email)
        user.score += score
        user.save() 
        