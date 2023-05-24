from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class SellerEditProfileTest(APITestCase):
    fixtures = ['accounts']
    edit_shop_url = reverse('accounts:edit_shop')
    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_edit_seller_profile_with_authentication_as_a_seller(self):
            
        #Arrange
        data = {'email': 'shop11@gmail.com',
                'username' : 'shop1',
                'user_phone_number':'09103335566',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "12345"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_edit_seller_profile_with_authentication_as_a_customer(self):
            
        #Arrange
        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {'email': 'shop11@gmail.com',
                'username' : 'shop1',
                'user_phone_number':'09103335566',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "12345"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)

    def test_edit_seller_profile_without_authentication(self):
            
        #Arrange
        self.client.force_authenticate(user=None , token = None)
        data = {'email': 'shop11@gmail.com',
                'username' : 'shop1',
                'user_phone_number':'09103335566',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "12345"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
        
    def test_edit_seller_profile_with_invalid_user_phone_number_with_authentication(self):
                
        #Arrange
        data = {'email': 'shop11@gmail.com',
                'username' : 'shop1',
                'user_phone_number':'091pp335566',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "12345"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_edit_seller_profile_with_invalid_email_with_authentication(self):
                
        #Arrange
        data = {'email': 'shop11gmail.com',
                'username' : 'shop1',
                'user_phone_number':'091pp335566',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "12345"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)



    def test_edit_seller_profile_with_invalid_shop_phone_number_with_authentication(self):
                
        #Arrange
        data = {'email': 'shop11@gmail.com',
                'username' : 'shop1',
                'user_phone_number':'09103335566',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "123ff45"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)