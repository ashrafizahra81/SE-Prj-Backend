from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class CustomerEditProfileTest(APITestCase):
    fixtures = ['accounts']
    edit_profile_url = reverse('accounts:edit-profile', kwargs={'type': "customer"})
    def setUp(self):

        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_edit_user_profile_shou_succeed_when_user_is_authenticated_and_data_is_valid(self):

        #Arrange
        data = {
                'email': 'golnoosh@gmail.com',
                'username' : 'golnooshasefi',
                'user_phone_number':'09103335566',
                'user_postal_code':'887799551',
                'user_address':'Isfahan',
                }
        #Act
        response = self.client.post(self.edit_profile_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
    def test_edit_user_profile_should_raise_error_when_user_is_not_authenticated(self):
    
        #Arrange
        self.client.force_authenticate(user=None , token = None)
        data = {
                'email': 'golnoosh@gmail.com',
                'username' : 'golnooshasefi',
                'user_phone_number':'09103335566',
                'user_postal_code':'887799551',
                'user_address':'Isfahan',
                }

        #Act
        response = self.client.post(self.edit_profile_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
    
    def test_edit_user_profile_should_raise_error_when_postal_code_is_invalid(self):
        
        #Arrange
        data = {
                'email': 'golnoosh@gmail.com',
                'username' : 'golnooshasefi',
                'user_phone_number':'09103335566',
                'user_postal_code':'sd12',
                'user_address':'Isfahan',
                }

        #Act
        response = self.client.post(self.edit_profile_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_edit_user_profile_should_raise_error_when_email_is_invalid(self):
        
        #Arrange
        data = {
                'email': 'golnooshgmail.com',
                'username' : 'golnooshasefi',
                'user_phone_number':'09103335566',
                'user_postal_code':'sd12',
                'user_address':'Isfahan',
                }

        #Act
        response = self.client.post(self.edit_profile_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_edit_user_profile_should_raise_error_when_phone_number_is_invalid(self):
            
        #Arrange
        data = {
                'email': 'golnoosh@gmail.com',
                'username' : 'golnooshasefi',
                'user_phone_number':'09103335kk6',
                'user_postal_code':'1245789636',
                'user_address':'Isfahan',
                }

        #Act
        response = self.client.post(self.edit_profile_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_edit_user_profile_should_succeed_when_user_enter_new_email(self):

        user = User.objects.get(id=1)
        user.user_address = 'Isfahan'
        user.user_postal_code = '12457896' 
        user.save()   
        #Arrange
        data = {
                'email': 'golnoosh3@gmail.com',
                'username' : 'golnoosh',
                'user_phone_number':'09108944555',
                'user_postal_code':'12457896',
                'user_address':'Isfahan',
                }

        #Act
        response = self.client.post(self.edit_profile_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , {  
                                            'email': 'golnoosh3@gmail.com',
                                            'username' : 'golnoosh',
                                            'user_phone_number':'09108944555',
                                            'user_postal_code':'12457896',
                                            'user_address':'Isfahan',
                                        })
        
