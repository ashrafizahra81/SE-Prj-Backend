from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class DeleteFromFavoriteProductsTest(APITestCase):
    fixtures = ['accounts' , 'products' , 'favoriteProducts']
    show_favorites_url = reverse('show-favorite')
    def setUp(self):
        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_show_favorite_products_with_authentication(self):

        #Arrange

        #Act
        response = self.client.get(self.show_favorites_url , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , [
                                            {
                                                "id": 1,
                                                "product_name": "T-shirt",
                                                "product_price": 120000,
                                                "product_off_percent": 0,
                                                "upload": "null"
                                            }
                                        ])

    def test_show_favorite_products_without_authentication(self):
    
        #Arrange
        self.client.force_authenticate(user=None , token = None)

        #Act
        response = self.client.get(self.show_favorites_url  , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)


    def test_show_favorite_products_with_authentication_with_empty_list(self):
    
        #Arrange
        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        #Act
        response = self.client.get(self.show_favorites_url , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
     