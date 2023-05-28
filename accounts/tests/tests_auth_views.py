from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from datetime import datetime

class UserAuthenticationTest(APITestCase):
    fixtures = ['accounts' , 'wallets']
    login_url = reverse('accounts:token_obtain_pair')
    register_url = reverse('accounts:register')
    create_shop_url = reverse('accounts:create_shop')
    verify_email_url = reverse('accounts:verify_email')
    verify_token_url = reverse('accounts:token_verify')
    def test_login_user_should_succeed_when_data_exist_as_a_customer(self):
        #Arrange
        data = {'email':'golnoosh@gmail.com',
                'password':'1234'}
        #Act
        response = self.client.post(self.login_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['type'] , 'user')

    def test_login_user_should_succeed_when_data_exist_as_a_seller(self):
        #Arrange
        data = {'email':'shop1@gmail.com',
                'password':'1234'}
        #Act
        response = self.client.post(self.login_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['type'] , 'seller')


    def test_login_user_with_shoul_raise_error_when_email_does_not_exist(self):
        #Arrange
        data = {'email':'golnoosh1@gmail.com',
                'password':'1234'}
        #Act
        response = self.client.post(self.login_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)


    def test_user_register_should_succeed_when_data_is_valid(self):
        #Arrange
        data = {
                "username": "maryam",
                "email":"maryam@gmail.com",
                "user_phone_number": "09107704555",
                "password":1234
                }
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)


    def test_user_register_should_raise_error_when_user_phone_number_is_invalid(self):
        #Arrange
        data = {
                "username": "maryam",
                "email":"maryam@gmail.com",
                "user_phone_number": "091077k555",
                "password":1234
                }
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    

    def test_user_register_should_raise_error_when_email_is_invalid(self):
            #Arrange
        data = {
                "username": "maryam",
                "email":"maryamgmail.com",
                "user_phone_number": "091077k555",
                "password":1234
                }
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_user_register_should_raise_error_when_email_is_duplicated_and_active(self):
        #Arrange
        data = {
                "username": "goli",
                "email":"golnoosh@gmail.com",
                "user_phone_number": "0910778555",
                "password":1234
                }
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_user_register_should_succeed_when_email_is_duplicated_and_inactive_and_usercode_has_expired(self):
        #Arrange
        data = {
                "username": "zahra_Ashrafi5",
                "email":"zarashrafi81@gmail.com",
                "user_phone_number": "0910779555",
                "password":1234
                }
        user = User.objects.get(email = "zarashrafi81@gmail.com")
        user.is_active = False
        user.save()
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)

    def test_user_register_should_succeed_when_email_is_duplicated_and_inactive_and_usercode_is_valid(self):
        #Arrange
        data = {
                "username": "mahlashams",
                "email":"shamsabadimahla@gmail.com",
                "user_phone_number": "0910179555",
                "password":1234
                }
        usercode = CodesForUsers.objects.get(email = 'shamsabadimahla@gmail.com')
        usercode.created_at = datetime.now()
        usercode.save()
        #Act
        response = self.client.post(self.register_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_202_ACCEPTED)


    def test_verify_email_should_raise_error_when_code_is_invalid(self):
        #Arrange
        data = {'code' : 1234}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    
    def test_verify_email_should_raise_error_when_code_does_not_exist(self):
        #Arrange
        data = {'code' : 123456}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)


    def test_verify_email_should_succeed_when_code_is_valid_and_user_is_customer(self):
        #Arrange
        data = {'code' : 710500}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual('shop_name' in response.data , False)


    def test_verify_email_should_succeed_when_code_is_valid_and_user_is_seller(self):
        #Arrange
        data = {'code' : 458269}
        #Act
        response = self.client.post(self.verify_email_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual('shop_name' in response.data , True)


    def test_user_create_shop_should_succeed_when_info_is_valid(self):
        #Arrange
        data = {
                "username": "shop7",
                "email":"shop7@gmail.com",
                "shop_name" : "shop7",
                "shop_address":"isfahan",
                "shop_phone_number": "09669949288",
                "password":1234
                }
        #Act
        response = self.client.post(self.create_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_user_create_shop_should_raise_error_when_email_is_invalid(self):
        #Arrange
        data = {
                "username": "shop7",
                "email":"shop7gmail.com",
                "shop_name" : "shop7",
                "shop_address":"isfahan",
                "shop_phone_number": "09669949288",
                "password":1234
                }
        #Act
        response = self.client.post(self.create_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_user_create_shop_should_raise_error_when_shop_phone_number_is_invalid(self):
        #Arrange
        data = {
                "username": "sho7",
                "email":"shop7@gmail.com",
                "shop_name" : "shop7",
                "shop_address":"isfahan",
                "shop_phone_number": "096699h9288",
                "password":1234
                }           
        #Act
        response = self.client.post(self.create_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_user_create_shop_should_raise_error_when_email_is_duplicated_and_active(self):
        #Arrange
        data = {
                "username": "shop3",
                "email":"shop3@gmail.com",
                "shop_name" : "shop3",
                "shop_address":"isfahan",
                "shop_phone_number": "09669959288",
                "password":1234
                } 
        #Act
        response = self.client.post(self.create_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_seller_register_should_succeed_when_email_is_duplicated_and_inactive_and_usercode_has_expired(self):
        #Arrange
        data = {
                "username": "shop3",
                "email":"shop3@gmail.com",
                "shop_name" : "shop3",
                "shop_address":"isfahan",
                "shop_phone_number": "09669959288",
                "password":1234
                } 
        user = User.objects.get(email = "shop3@gmail.com")
        user.is_active = False
        user.save()
        #Act
        response = self.client.post(self.create_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)

    def test_seller_register_should_succeed_when_email_is_duplicated_and_inactive_and_usercode_is_valid(self):
        #Arrange
        data = {
                "username": "shop3",
                "email":"shop3@gmail.com",
                "shop_name" : "shop3",
                "shop_address":"isfahan",
                "shop_phone_number": "09669959288",
                "password":1234
                } 
        user = User.objects.get(email = "shop3@gmail.com")
        user.is_active = False
        user.save()
        usercode = CodesForUsers.objects.get(email = 'shop3@gmail.com')
        usercode.created_at = datetime.now()
        usercode.save()
        #Act
        response = self.client.post(self.create_shop_url , data , format = 'json')

        #Assert
        self.assertEqual(response.status_code , status.HTTP_202_ACCEPTED)


    def test_token_verification_should_succeed_when_token_is_valid(self):
        #Arrange
        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {'token' : str(self.access_token)}

        #Act
        response = self.client.post(self.verify_token_url , data , format = 'json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)