from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from orders.models import Order
from wallets.models import Wallet
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestCheckout(APITestCase):

    fixtures = ['accounts' , 'products', 'orders', 'wallets', 'shoppingCarts']
    checkout_urls = reverse('checkout')

    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_checkout_with_authentication_and_not_enough_money_in_wallet(self):

        data = {'type': 'wallet'}

        response = self.client.post(self.checkout_urls, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {
                                            "message": "موجودی کیف پول شما برای این خرید کافی نیست"
                                        }
                        )
    
    # def test_checkout_with_authentication_and_enough_money_in_wallet(self):

    #     self.user = User.objects.get(id=3)
    #     self.access_token = AccessToken.for_user(self.user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    #     data = {'type': 'wallet'}

    #     response = self.client.post(self.checkout_urls, data,  format = 'json')
    #     self.assertEqual(response.status_code , status.HTTP_200_OK)
    #     self.assertEqual(response.data, {
    #                                         "message": "خرید با موفقیت انجام شد", 
    #                                         "balance": 120000.0
    #                                     }
    #                     )
    

    def test_checkout_without_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        data = {'type': 'wallet'}

        response = self.client.post(self.checkout_urls, data,format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    