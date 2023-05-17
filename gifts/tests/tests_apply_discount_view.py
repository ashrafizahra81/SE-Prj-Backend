from rest_framework.test import APITestCase
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from datetime import date


class ShowGiftTest(APITestCase):
    fixtures = ['accounts' , 'gifts' ,'shoppingCart','products']
    apply_discount_url = reverse('apply_discount')
    

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_apply_discount_type_A_with_authentication(self):
        
        #Arrange
        data = {'discount_code':'DG4T5H'}
        #Act
        response = self.client.post(self.apply_discount_url , data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , {
                                            "total_cost": 470000.0,
                                            "discounted_total_cost": 376000.0,
                                            "shippingPrice": 30000
                                        })
        
    def test_apply_discount_without_authentication(self):

        #Arrange
        self.client.force_authenticate(user=None , token = None)
        data = {'discount_code':'DG4T5H'}
        #Act
        response = self.client.post(self.apply_discount_url , data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)


    def test_apply_discount_with_invalid_code_with_authentication(self):
        
        #Arrange
        self.user = User.objects.get(id=3)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {'discount_code':'V4D9X85'}
        #Act
        response = self.client.post(self.apply_discount_url , data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)