from .user_interface import UserService

class ConcreteUserService(UserService):

    def updateUser(self, serialized_data, is_valid):
        
        account = serialized_data.save()
        account.is_active = is_valid
        account.save()