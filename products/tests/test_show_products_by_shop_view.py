from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestShowProductsByShop(APITestCase):

    fixtures = ['accounts', 'products']
    show_products_to_shop_urls = reverse('show-products-of-shop')

    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))


    def test_show_products_to_a_shop_manager(self):

        response = self.client.get(self.show_products_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                                            "products": [
                                                {
                                                    "id": 1,
                                                    "product_name": "T-shirt",
                                                    "product_price": 120000,
                                                    "product_off_percent": 0,
                                                    "inventory": 5,
                                                    "upload": "null",
                                                    "shop_id": 4
                                                },
                                                {
                                                    "id": 3,
                                                    "product_name": "pants",
                                                    "product_price": 620000,
                                                    "product_off_percent": 0,
                                                    "inventory": 15,
                                                    "upload": "null",
                                                    "shop_id": 4
                                                },
                                                {
                                                    "id": 4,
                                                    "product_name": "pants",
                                                    "product_price": 400000,
                                                    "product_off_percent": 0,
                                                    "inventory": 18,
                                                    "upload": "null",
                                                    "shop_id": 4
                                                },
                                                {
                                                    "id": 5,
                                                    "product_name": "T-shirt",
                                                    "product_price": 110000,
                                                    "product_off_percent": 0,
                                                    "inventory": 19,
                                                    "upload": "null",
                                                    "shop_id": 4
                                                },
                                                {
                                                    "id": 15,
                                                    "product_name": "pants",
                                                    "product_price": 2330000,
                                                    "product_off_percent": 0,
                                                    "inventory": 10,
                                                    "upload": "null",
                                                    "shop_id": 4
                                                }
                                            ],
                                            "shop_name": "shop1",
                                            "shop_address": "isfahan",
                                            "shop_phone_number": "09808949238"
                                        })

    def test_show_products_to_a_user_who_is_not_a_shop_manager(self): 

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.show_products_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
                                            "detail": "You do not have permission to perform this action."
                                        })


    def test_show_products_without_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.show_products_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)