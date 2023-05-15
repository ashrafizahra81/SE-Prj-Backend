from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class UserAuthenticationTest(APITestCase):
    fixtures = ['accounts' , 'wallets']
    login_url = reverse('accounts:token_obtain_pair')
    
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