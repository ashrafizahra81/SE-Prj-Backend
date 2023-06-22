from abc import ABC, abstractmethod


class CodeForUsersService(ABC):
    
    @abstractmethod
    def updateCodesForUsers(self, token, email, date):
        pass

    @abstractmethod
    def createCodesForUsers(self, token, email, date):
        pass

class EditProfileService(ABC):

    @abstractmethod
    def edit_profile(slf, serialized_data):
        pass

class MailService(ABC):
    @abstractmethod
    def send_mail(self, html, text, subject, from_email, to_emails):
        pass

    @abstractmethod
    def sendEmail(self, email):
        pass
class RegisterService(ABC):

    @abstractmethod
    def userRegister(self, email):
        pass

class CheckEmailForRegister(ABC):

    @abstractmethod
    def checkIfEmailExists(self, email):
        pass

class SaveNewUser(ABC):

    @abstractmethod
    def saveNewUser(self, serialized_data, email, phone_number):
        pass

class ResetPasswordService(ABC):

    def reset_password(self, request):
        pass

class ShowUserInfoService(ABC):

    @abstractmethod
    def show_user_info(self, user_id):
        pass

class UniqueCodeService(ABC):
    @abstractmethod
    def getUniqueCode(self):
        pass

class UserService(ABC):

    @abstractmethod
    def updateUser(self, serialized_data, is_valid):
        pass
    @abstractmethod
    def updateUserScore(self , score , email):
        pass
    @abstractmethod
    def updateUserIsValid(self, user, is_valid):
        pass
    @abstractmethod
    def updateUserPassword(self, user, password):
        pass
    @abstractmethod
    def updateUserCode(self, user, code):
        pass

class VerfyUserToResgisterService(ABC):

    @abstractmethod
    def verify_user_to_register(self, code):
        pass
