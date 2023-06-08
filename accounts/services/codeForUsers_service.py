from accounts.models import CodesForUsers
from .codeForUsers_interface import CodeForUsersService
from datetime import datetime


class ConcreteCodeForUsersService(CodeForUsersService):

    def checkIfTheCodeExists(self, token):
        return CodesForUsers.objects.filter(code=token).exists()

    def createCodesForUsers(self, token, email, date):
        user_code = CodesForUsers(
            code = token,
            created_at = date,
            email = email 
        )
        user_code.save()
    
    def updateCodesForUsers(self, token, email, date):
        userCode = CodesForUsers.objects.get(email = email)
        userCode.created_at = date
        userCode.code = token
        userCode.save()

    def hasExpired(self, email):
        userCode = CodesForUsers.objects.get(email = email)
        now = datetime.now()
        delta = now - userCode.created_at.replace(tzinfo=None)
        diff = delta.seconds

        return diff > 600