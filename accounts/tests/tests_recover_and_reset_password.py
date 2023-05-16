from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User , CodesForUsers
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class ChangePasswordTest(APITestCase):
    fixtures = ['accounts']
    reset_password_url = reverse('accounts:reset_password')
    recover_password_url = reverse('accounts:recover_password' , args=[4])

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.codeforusers = CodesForUsers.objects.get(id=4)

    def test_get_token_to_reset_password_with_authentication(self):
        #Arrange
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        #Act
        response = self.client.get(self.reset_password_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        

    def test_get_token_to_reset_password_without_authentication(self):

        #Arrange

        #Act
        response = self.client.get(self.reset_password_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)


    def test_change_password_by_entering_code_from_email_with_authentication(self):
        #Arrange
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {"token":self.user.random_integer,
                "password":"12345",
                "password2":"12345"}
        #Act
        response = self.client.post(self.reset_password_url , data=data , format='json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_change_password_by_entering_invalid_code_from_email_with_authentication(self):
        #Arrange
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {"token":self.user.random_integer+1,
                "password":"12345",
                "password2":"12345"}
        #Act
        response = self.client.post(self.reset_password_url , data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    

    def test_change_password_by_entering_non_matching_passwords_with_authentication(self):
        #Arrange
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        print(self.user.random_integer)
        data = {"token":self.user.random_integer,
                "password":"12345",
                "password2":"123456"}
        #Act
        response = self.client.post(self.reset_password_url , data=data , format='json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    
    def test_recover_password_by_entering_invalid_code_from_email(self):
        #Arrange
        data = {"token":self.codeforusers.code+'1',
                "password":"12345",
                "password2":"12345"}
        #Act
        response = self.client.post(self.recover_password_url , data=data , format='json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_recover_password_by_entering_non_matching_passwords(self):
        #Arrange
        data = {"token":self.codeforusers.code,
                "password":"123456",
                "password2":"12345"}
        #Act
        response = self.client.post(self.recover_password_url , data=data , format='json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_recover_password_by_entering_valid_data(self):
        #Arrange
        
        data = {"token":self.codeforusers.code,
                "password":"12345",
                "password2":"12345"}
        #Act
        response = self.client.post(self.recover_password_url , data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

