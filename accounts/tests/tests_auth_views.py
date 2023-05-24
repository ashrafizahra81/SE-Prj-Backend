from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from datetime import datetime

class UserAuthenticationTest(APITestCase):
    fixtures = ['accounts' , 'wallets']
    login_url = reverse('accounts:token_obtain_pair')
    register_url = reverse('accounts:register')
    verify_email_url = reverse('accounts:verify_email')
    
    def test_login_user_with_existed_data(self):
        #Arrange
        data = {'email':'golnoosh@gmail.com',
                'password':'1234'}
        #Act
        response = self.client.post(self.login_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
    def test_login_user_with_non_existed_data(self):
        #Arrange
        data = {'email':'golnoosh1@gmail.com',
                'password':'1234'}
        #Act
        response = self.client.post(self.login_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)


    def test_user_register_with_valid_info_without_duplicated_email(self):
        #Arrange
        data = {
                "username": "maryam",
                "email":"maryam@gmail.com",
                "user_phone_number": "09107704555",
                "password":1234
                }
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)


    def test_user_register_without_valid_info_without_duplicated_email(self):
        #Arrange
        data = {
                "username": "maryam",
                "email":"maryam@gmail.com",
                "user_phone_number": "091077k555",
                "password":1234
                }
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    # def test_user_register_with_duplicated_and_active_email_(self):
    #     #Arrange
    #     data = {
    #             "username": "goli",
    #             "email":"golnoosh@gmail.com",
    #             "user_phone_number": "0910778555",
    #             "password":1234
    #             }
    #     #Act
    #     response = self.client.post(self.register_url , data , format = 'json')

    #     #Assert
    #     self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_user_register_with_duplicated_and_inactive_email_with_expired_code(self):
        #Arrange
        data = {
                "username": "zahra_Ashrafi5",
                "email":"zarashrafi81@gmail.com",
                "user_phone_number": "0910779555",
                "password":1234
                }
        user = User.objects.get(email = "zarashrafi81@gmail.com")
        user.is_active = False
        user.save()
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)

    def test_user_register_with_duplicated_and_inactive_email_with_unexpired_code(self):
        #Arrange
        data = {
                "username": "mahlashams",
                "email":"shamsabadimahla@gmail.com",
                "user_phone_number": "0910179555",
                "password":1234
                }
        usercode = CodesForUsers.objects.get(email = 'shamsabadimahla@gmail.com')
        usercode.created_at = datetime.now()
        usercode.save()
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_202_ACCEPTED)


    def test_verify_email_with_invalid_code(self):
        #Arrange
        data = {'code' : 1234}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    
    # def test_verify_email_with_expired_code(self):
    #     #Arrange
    #     data = {'code' : 506200}
    #     #Act
    #     response = self.client.post(self.verify_email_url , data , format = 'json')

    #     #Assert
    #     self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_verify_email_with_valid_code_as_a_customer(self):
        #Arrange
        data = {'code' : 710500}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual('shop_name' in response.data , False)


    def test_verify_email_with_valid_code_as_a_seller(self):
        #Arrange
        data = {'code' : 458269}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual('shop_name' in response.data , True)

