from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from shoppingCarts.models import UserShoppingCart
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestAddToCart(APITestCase):

    fixtures = ['accounts', 'products', 'shoppingCarts']
    add_to_cart_url = reverse('add-to-cart')

    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_add_to_cart_with_authentication_and_existing_product(self):

        data = {'data': 1}

        response = self.client.post(self.add_to_cart_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        self.assertEqual(response.data, {"message": "محصول مورد نظر به سبد خرید اضافه شد"})
    
    def test_add_to_cart_with_authentication_and_non_existing_product(self):

        data = {'data': 8}

        response = self.client.post(self.add_to_cart_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        self.assertEqual(response.data, {"message": "محصول مورد نظر موجود نیست"} )
    
    def test_add_to_cart_with_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        data = {'data': 1}

        response = self.client.post(self.add_to_cart_url, data,format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
    
    def test_add_to_cart_without_authentication(self):


        self.client.force_authenticate(user=None , token = None)

        data = {'data': 1}

        response = self.client.post(self.add_to_cart_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
