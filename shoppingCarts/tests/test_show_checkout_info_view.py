from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from shoppingCarts.models import UserShoppingCart
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestShowCheckoutInfo(APITestCase):
    
    fixtures = ['accounts', 'shoppingCarts', 'products']
    show_checkout_info_url = reverse('show-checkout-info')

    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_show_checkout_info_with_authentication(self):

        response = self.client.get(self.show_checkout_info_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                                            "discounted_price": 620000.0,
                                            "total_cost": 650000.0,
                                            "score": 6,
                                            "shippingPrice": 30000
                                        })
    
    def test_show_checkout_info_with_authentication_and_changed_cart(self):

        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.show_checkout_info_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {
                                            "message": "سبد خرید شما تغییر یافته است"
                                        })
    
    def test_show_checkout_info_without_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.show_checkout_info_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    def test_show_checkout_info_with_authentication_but_has_nothing_in_cart(self):

        self.user = User.objects.get(id=3)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.show_checkout_info_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                                            "discounted_price": 0,
                                            "total_cost": 30000,
                                            "score": 0,
                                            "shippingPrice": 30000
                                        })