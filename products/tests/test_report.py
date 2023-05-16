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

    def test_show_reports_to_a_shop_manager(self):

        response = self.client.get(self.report_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, [
                                            {
                                                "productName": "T-shirt",
                                                "inventory": 5,
                                                "initial_inventory": 12,
                                                "price": 120000,
                                                "totalPriceOfProduct": 840000,
                                                "date": datetime.date(2023,5,14)
                                            },
                                            {
                                                "productName": "hoodie",
                                                "inventory": 5,
                                                "initial_inventory": 5,
                                                "price": 320000,
                                                "totalPriceOfProduct": 0,
                                                "date": "تاکنون خریدی انجام نشده"
                                            },
                                            {
                                                "productName": "pants",
                                                "inventory": 15,
                                                "initial_inventory": 15,
                                                "price": 620000,
                                                "totalPriceOfProduct": 0,
                                                "date": "تاکنون خریدی انجام نشده"
                                            },
                                            {
                                                "productName": "pants",
                                                "inventory": 18,
                                                "initial_inventory": 18,
                                                "price": 400000,
                                                "totalPriceOfProduct": 0,
                                                "date": "تاکنون خریدی انجام نشده"
                                            },
                                            {
                                                "productName": "T-shirt",
                                                "inventory": 19,
                                                "initial_inventory": 19,
                                                "price": 110000,
                                                "totalPriceOfProduct": 0,
                                                "date": "تاکنون خریدی انجام نشده"
                                            },
                                            {
                                                "productName": "pants",
                                                "inventory": 10,
                                                "initial_inventory": 10,
                                                "price": 2330000,
                                                "totalPriceOfProduct": 0,
                                                "date": "تاکنون خریدی انجام نشده"
                                            },
                                            {
                                                "totalSell": 840000
                                            }
                                        ])
    
    def test_show_reports_to_a_user_who_is_not_a_shop_manager(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.report_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
                                            "detail": "You do not have permission to perform this action."
                                        })
    

    def test_show_reports_without_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.report_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)