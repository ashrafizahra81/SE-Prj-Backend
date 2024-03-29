from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestFilter(APITestCase):

    fixtures = ['accounts', 'products']
    filters_url = reverse('filters')

    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
    
    def test_filters_should_succeed_with_authentication_when_there_are_not_any_matching_products(self):

        data = {
            'group': ['shirt']
        }

        response = self.client.post(self.filters_url, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)

    def test_filters_should_succeed_with_authentication_when_there_are_some_matching_products(self):

        data = {
            'group': ['pants']
        }

        response = self.client.post(self.filters_url, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, [
                {
                    "id": 3,
                    "product_name": "pants",
                    "product_price": 620000,
                    "upload": "https://s29.picofile.com/file/8462060092/images.jpg",
                    "shop_id": 4
                },
                {
                    "id": 4,
                    "product_name": "pants",
                    "product_price": 400000,
                    "upload": "https://s28.picofile.com/file/8462477126/DSC_7010_91576.jpg",
                    "shop_id": 4
                },
                {
                    "id": 8,
                    "product_name": "pants",
                    "product_price": 550000,
                    "upload": "https://s28.picofile.com/file/8462477118/8228022250_6_1_1.jpg",
                    "shop_id": 5
                },
                {
                    "id": 13,
                    "product_name": "pants",
                    "product_price": 3180000,
                    "upload": "https://s29.picofile.com/file/8462477084/2.jpg",
                    "shop_id": 6
                },
                {
                    "id": 14,
                    "product_name": "pants",
                    "product_price": 3880000,
                    "upload": "https://s28.picofile.com/file/8462477076/1.jpg",
                    "shop_id": 6
                }
            ]
        )

    def test_filters_should_raise_error_when_the_user_has_not_been_authorized(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.filters_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)