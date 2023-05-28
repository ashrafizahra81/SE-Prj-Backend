from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from shoppingCarts.models import UserShoppingCart
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestDeleteFromCart(APITestCase):

    fixtures = ['accounts', 'shoppingCarts', 'products']
    delete_from_cart_url = reverse('delete-from-cart')

    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
    
    def test_delete_from_cart_should_succeed_when_with_authentication(self):

        data = {'data': 3}

        response = self.client.post(self.delete_from_cart_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        self.assertEqual(response.data, {"message": "محصول مورد نظر با موفقیت از سبد خرید حذف شد"} )

    def test_delete_from_cart_should_raise_error_when_without_authentication(self):


        self.client.force_authenticate(user=None , token = None)

        data = {'data': 3}

        response = self.client.post(self.delete_from_cart_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
