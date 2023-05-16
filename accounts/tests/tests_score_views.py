from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class ScoreTest(APITestCase):
    fixtures = ['accounts']
    show_score_url = reverse('accounts:show_score')
    def setUp(self):

        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_show_score_with_authentication(self):
            
        #Arrange

        #Act
        response = self.client.get(self.show_score_url)

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['score'] , 0)

    def test_show_score_without_authentication(self):
            
        #Arrange
        self.client.force_authenticate(user=None , token = None)
        #Act
        response = self.client.get(self.show_score_url)

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)