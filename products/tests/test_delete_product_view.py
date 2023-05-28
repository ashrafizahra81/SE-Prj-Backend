from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestDeleteProduct(APITestCase):

    fixtures = ['accounts' , 'products']
    delete_product_url = reverse('delete-product', kwargs={'pk': 1})
    
    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_delete_product_by_shop_owner_should_succeed_when_the_user_has_been_authorized(self):

        response = self.client.delete(self.delete_product_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data,{'message': 'محصول موردنظر با موفقیت حذف شد'})
    
    def test_delete_product_should_raise_error_when_the_user_has_not_been_authorized(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.delete(self.delete_product_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)