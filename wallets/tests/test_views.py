from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestWallet(APITestCase):

    fixtures = ['accounts' , 'wallets']
    charge_wallet_url = reverse('charge_wallet')

    def setUp(self):

        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_charge_wallet_should_succeed_when_user_is_authenticated(self):

        #Arrange
        data = {'insert': 100}

        #Act
        response = self.client.post(self.charge_wallet_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_charge_wallet_should_raise_erro_when_user_is_not_authenticated(self):
    
        #Arrange
        self.client.force_authenticate(user=None , token = None)
        data = {'insert': 100}

        #Act
        response = self.client.post(self.charge_wallet_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    def test_charge_wallet_should_raise_error_when_data_is_invalid(self):

        #Arrange
        data = {'insert':0}

        #Act
        response = self.client.post(self.charge_wallet_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)