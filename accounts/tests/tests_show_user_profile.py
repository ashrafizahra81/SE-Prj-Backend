from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class ScoreTest(APITestCase):
    fixtures = ['accounts' , 'wallets']
    show_user_info_url = reverse('accounts:show_user_info')
    def setUp(self):

        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
    def test_show_customer_profile_with_authentication(self):
    
        #Arrange

        #Act
        response = self.client.get(self.show_user_info_url)

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data ,{
                                            "email": "golnoosh@gmail.com",
                                            "username": "golnoosh",
                                            "user_phone_number": "09108944555",
                                            "user_postal_code": None,
                                            "user_address": None,
                                            "inventory": 0.0
                                        })
        
    def test_show_seller_profile_with_authentication(self):
        
        #Arrange
        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        #Act
        response = self.client.get(self.show_user_info_url)

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data ,{
                                            "email": "shop1@gmail.com",
                                            "username": "shop1",
                                            "shop_name": "shop1",
                                            "shop_phone_number": "09808949238",
                                            "user_phone_number": None,
                                            "shop_address": "isfahan"
                                        })
        
    def test_show_user_profile_without_authentication(self):
            
        #Arrange
        self.client.force_authenticate(user=None , token = None)

        #Act
        response = self.client.get(self.show_user_info_url)

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)