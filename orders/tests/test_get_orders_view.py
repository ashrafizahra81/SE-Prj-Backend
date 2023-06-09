from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from orders.models import Order
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestGetOrders(APITestCase):

    fixtures = ['accounts' , 'products', 'orders']
    get_orders_urls = reverse('user-orders')
    
    def setUp(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
    
    def test_get_orders_with_authentication_should_succeed_when_some_orders_exist(self):

        #Act
        response = self.client.get(self.get_orders_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data , [
                                            {
                                                "id": 1,
                                                "product_name": "T-shirt",
                                                "product_price": 120000,
                                                # "upload": "null",
                                                "inventory": 5,
                                                # "initial_inventory": 12,
                                                "product_size": "38",
                                                "product_group": "T-shirt",
                                                "product_image": "https://s28.picofile.com/file/8462477276/u1ktrbrvf0_rvca_f_4409_frt1.jpg",
                                                "product_color": "multi color",
                                                "product_height": 20,
                                                "product_design": "striped",
                                                "product_material": "cotton",
                                                "product_country": "Iran",
                                                # "product_off_percent": 0,
                                                # "is_available": True,
                                                # "is_deleted": False,
                                                # "score": 0.0,
                                                # "number_of_votes": 0,
                                                # "last_product_sold_date": "2023-05-14T20:40:01.126548Z",
                                                # "shop": 4,
                                                "cost": 120000,
                                                # "order_date": "2023-05-15T03:40:01.296070Z",
                                                # "complete_date": "2023-05-15T03:40:01.296070Z",
                                                "status": "Accepted"
                                            }
                                        ])
    def test_get_orders_with_authentication_should_succeed_when_there_are_not_any_orders(self):
        
        self.user = User.objects.get(id=1)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.get(self.get_orders_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)

    def test_get_orders_should_raise_error_when_the_user_has_not_been_authorized(self):

        self.client.force_authenticate(user=None , token = None)
        response = self.client.get(self.get_orders_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    