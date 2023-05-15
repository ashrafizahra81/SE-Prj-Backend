from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class ChangePasswordTest(APITestCase):
    fixtures = ['accounts']
    reset_password_url = reverse('accounts:reset_password')
    def setUp(self):

        self.user = User.objects.get(id=1)
        print(self.user)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_get_token_to_reset_password_with_authentication(self):
        #Arrange

        #Act
        response = self.client.get(self.reset_password_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        

    def test_get_token_to_reset_password_without_authentication(self):

        #Arrange
        self.client.force_authenticate(user=None , token = None)
        #Act
        response = self.client.get(self.reset_password_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)


    def test_change_password_by_entering_code_from_email_with_authentication(self):
        #Arrange
        print(self.user.random_integer)
        data = {"token":self.user.random_integer,
                "password":"12345",
                "password2":"12345"}
        #Act
        response = self.client.post(self.reset_password_url , data=data , format='json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_change_password_by_entering_invalid_code_from_email_with_authentication(self):
            #Arrange
        print(self.user.random_integer)
        data = {"token":self.user.random_integer,
                "password":"12345",
                "password2":"12345"}
        #Act
        response = self.client.post(self.reset_password_url , data=data , format='json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
    