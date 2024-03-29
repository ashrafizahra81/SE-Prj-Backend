from rest_framework.test import APITestCase
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from datetime import date , timedelta


class ShowGiftTest(APITestCase):
    fixtures = ['accounts' , 'gifts']
    show_gift_url = reverse('show_gift')
    get_gift_url = reverse('get_gift')

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_show_gift_should_succeed_when_user_is_authenticated(self):
        
        #Arrange
        gift = Gift.objects.get(pk = 2)
        gift.date = datetime.now() + timedelta(days=20)
        gift.save()
        #Act
        response = self.client.get(self.show_gift_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , [
                                            {
                                                "description": "تخفیف 30 درصدی",
                                                "score": 200,

                                                "date": (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),

                                                "date": '2023-07-12'

                                            }
                                        ])

    def test_show_gift_should_raise_error_when_user_is_not_authenticated(self):
        #Arrange
        self.client.force_authenticate(user=None , token = None)
        #Act
        response = self.client.get(self.show_gift_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    def test_show_gift_should_succeed_when_list_of_gifts_is_empty(self):
        #Arrange
        gifts = Gift.objects.all()
        for i in gifts:
            i.delete()
        #Act
        response = self.client.get(self.show_gift_url)
        #Assert
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)

    def test_get_gift_should_succeed_when_score_is_valid_and_user_is_authenticated(self):
        #Arrange
        data = {'score': 200}
        user = User.objects.get(id = 1)
        user.score = 250
        user.save()
        #Act
        response = self.client.post(self.get_gift_url,data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , {'discount_code':'HJ61R9B' , 'new_score':50})


    def test_get_gift_should_raise_error_when_score_is_not_valid(self):
        #Arrange
        data = {'score': 'a100'}
        #Act
        response = self.client.post(self.get_gift_url,data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_get_gift_should_succeed_when_score_of_user_is_not_enough(self):
        #Arrange
        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        data = {'score': 100}
        #Act
        response = self.client.post(self.get_gift_url,data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)

    def test_get_gift_should_raise_error_when_user_is_not_authenticated(self):
        #Arrange
        self.client.force_authenticate(user=None , token = None)
        data = {'score': 100}
        #Act
        response = self.client.post(self.get_gift_url,data=data , format='json')
        #Assert
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)