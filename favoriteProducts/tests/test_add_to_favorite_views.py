from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class FavoriteProductsTest(APITestCase):
    fixtures = ['accounts' , 'products']
    add_to_favorite_url = reverse('add-to-favorite')
    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        
    def test_add_to_favoriteProducts_should_succeed_when_user_is_authenticated(self):

        #Arrange
        data = {'data': 1}

        #Act
        response = self.client.post(self.add_to_favorite_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
    
    def test_add_to_favoriteProducts_should_raise_error_when_user_is_not_authenticated(self):

        #Arrange
        self.client.force_authenticate(user=None , token = None)
        data = {'data': 1}

        #Act
        response = self.client.post(self.add_to_favorite_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    def test_add_to_favoriteProducts_should_raise_error_when_id_of_product_does_not_exist(self):

        #Arrange
        data = {'data': 22}

        #Act
        response = self.client.post(self.add_to_favorite_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)        