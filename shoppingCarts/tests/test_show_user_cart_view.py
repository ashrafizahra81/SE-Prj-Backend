from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from shoppingCarts.models import UserShoppingCart
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestShowUserCart(APITestCase):

    fixtures = ['accounts', 'shoppingCarts', 'products']
    show_user_cart_url = reverse('show-cart')

    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
    
    def test_show_user_cart_should_succeed_when_with_authentication(self):

        response = self.client.get(self.show_user_cart_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                                            "products": [
                                                {
                                                    "id": 3,
                                                    "product_name": "pants",
                                                    "product_size": "38",
                                                    "product_color": "ice blue",
                                                    "product_price": 620000,
                                                    "is_available": True,
                                                    "upload": None,
                                                    "shop_id": 4,
                                                    "product_off_percent": 620000.0
                                                }
                                            ],
                                            "total_price": 620000,
                                            "total_price_with_discount": 620000.0
                                        })
    
    def test_show_user_cart_should_raise_error_when_without_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.show_user_cart_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
    
    def test_show_user_cart_should_succeed_when_with_authentication_and_an_empty_cart(self):
        
        self.user = User.objects.get(id=3)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.show_user_cart_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)