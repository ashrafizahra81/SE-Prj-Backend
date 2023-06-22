from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class SellerEditProfileTest(APITestCase):
    fixtures = ['accounts']
    edit_shop_url = reverse('accounts:edit-profile', kwargs={'type': "shop"})
    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_edit_seller_profile_should_succeed_when_seller_is_authenticated(self):
            
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


    def test_edit_seller_profile_should_succeed_when_new_phone_number_entered(self):
            
        #Arrange
        user = User.objects.get(id = 4)
        user.shop_address = "isfahan77"
        user.user_phone_number = '09103445680'
        data = {'email': 'shop1@gmail.com',
                'username' : 'shop1',
                'user_phone_number':'09103445680',
                "shop_name": "shop1",
                "shop_address": "isfahan77",
                "shop_phone_number": "09808949238"
                }

        #Act
        response = self.client.post(self.edit_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , {  'email': 'shop1@gmail.com',
                                            'username' : 'shop1',
                                            'user_phone_number':'09103445680',
                                            "shop_name": "shop1",
                                            "shop_address": "isfahan77",
                                            "shop_phone_number": "09808949238"
                                        })

    def test_edit_seller_profile_should_raise_error_when_user_does_not_have_permission(self):
            
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

    def test_edit_seller_profile_should_raise_error_when_user_is_not_authenticated(self):
            
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
        
    def test_edit_seller_profile_should_raise_error_when_user_phone_number_is_invalid(self):
                
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


    def test_edit_seller_profile_should_raise_error_when_email_is_invalid(self):
                
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



    def test_edit_seller_profile_should_raise_error_when_shop_phone_number_is_invalid(self):
                
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