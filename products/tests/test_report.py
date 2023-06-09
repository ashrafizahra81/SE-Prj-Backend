from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
import datetime

class TestReport(APITestCase):

    fixtures = ['accounts', 'products']
    report_url = reverse('report')

    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_show_reports_should_succeed_when_to_a_shop_manager(self):

        response = self.client.get(self.report_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, [
                {
                    "product_name": "T-shirt",
                    "inventory": 5,
                    "initial_inventory": 12,
                    "product_price": 120000,
                    "date": datetime.date(2023, 5, 14),
                    "totalPriceOfProduct": 840000
                },
                {
                    "product_name": "pants",
                    "inventory": 15,
                    "initial_inventory": 15,
                    "product_price": 620000,
                    "date": "تاکنون خریدی انجام نشده",
                    "totalPriceOfProduct": 0
                },
                {
                    "product_name": "pants",
                    "inventory": 18,
                    "initial_inventory": 18,
                    "product_price": 400000,
                    "date": "تاکنون خریدی انجام نشده",
                    "totalPriceOfProduct": 0
                },
                {
                    "product_name": "T-shirt",
                    "inventory": 19,
                    "initial_inventory": 19,
                    "product_price": 110000,
                    "date": "تاکنون خریدی انجام نشده",
                    "totalPriceOfProduct": 0
                },
                {
                    "totalSell": 840000
                }
            ]
        )
    
    def test_show_reports_should_raise_error_when_to_a_user_who_is_not_a_shop_manager(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.report_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
                                            "detail": "You do not have permission to perform this action."
                                        })
    

    def test_show_reports_should_raise_error_when_the_user_has_not_been_authorized(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.report_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)