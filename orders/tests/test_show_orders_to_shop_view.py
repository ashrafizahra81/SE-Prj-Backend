from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from orders.models import Order
from wallets.models import Wallet
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestShowOrdersToShop(APITestCase):

    fixtures = ['accounts', 'orders', 'products']
    show_orders_to_shop_urls = reverse('show-order-to-shop')

    def setUp(self):
        
        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    
    def test_show_orders_to_shop_should_succeed_when_the_user_has_been_authorized(self):

        response = self.client.get(self.show_orders_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, [
                                            {
                                                "id": 1,
                                                "product_name": "T-shirt",
                                                "product_size": "38",
                                                "product_color": "multi color",
                                                "product_price": 120000,
                                                "inventory": 5,
                                                "upload": "https://s28.picofile.com/file/8462477276/u1ktrbrvf0_rvca_f_4409_frt1.jpg",
                                                "shop_id": 4
                                            }
                                        ])
    
    def test_show_orders_to_shop_should_raise_error_when_the_user_has_not_been_authorized(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.show_orders_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    # def test_show_orders_to_a_user_which_is_not_a_shop(self):

    def test_show_orders_to_shop_with_authentication_should_succeed_when_there_are_not_any_orders(self):


        self.user = User.objects.get(id=5)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.get(self.show_orders_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        