from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken


class TestEditProduct(APITestCase):

    fixtures = ['accounts', 'products']
    edit_product_url = reverse('edit-product', kwargs={'pk': 4})

    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    
    def test_edit_product_with_valid_data(self):

        data = {
                "product_name": "pants",
                "product_price": "2330000",
                "product_size": "36",
                "product_color": "light blue",
                "product_height": "100",
                "product_design": "plain",
                "product_material": "denim",
                "product_country": "Iran",
                "inventory": "5",
                "product_off_percent": "0",
                "is_available": "1"
                }
        
        response = self.client.put(self.edit_product_url, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                                            "product_name": "",
                                            "product_price": 2330000,
                                            "inventory": 5,
                                            "product_size": "",
                                            "product_color": "",
                                            "product_height": "",
                                            "product_design": "",
                                            "product_material": "",
                                            "product_country": "",
                                            "product_off_percent": "",
                                            "is_available": ""
                                        })
    
    def test_edit_product_with_invalid_data(self):

        data = {
                "product_name": "pants",
                "product_price": "2330000 dollar",
                "product_size": "36",
                "product_color": "light blue",
                "product_height": "100",
                "product_design": "plain",
                "product_material": "denim",
                "product_country": "Iran",
                "inventory": "5",
                "product_off_percent": "0",
                "is_available": "1"
                }
        
        response = self.client.put(self.edit_product_url, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    
    def test_edit_product_with_valid_data_2(self):

        data = {
                "product_name": "T-shirt",
                "product_price": "400000",
                "product_size": "38",
                "product_color": "red",
                "product_height": "110",
                "product_design": "striped",
                "product_material": "cotton",
                "product_country": "Turkey",
                "inventory": "18",
                "product_off_percent": "20",
                "is_available": "0"
                }
        
        response = self.client.put(self.edit_product_url, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                                            "product_name": "T-shirt",
                                            "product_price": "",
                                            "inventory": "",
                                            "product_size": "38",
                                            "product_color": "red",
                                            "product_height": 110,
                                            "product_design": "striped",
                                            "product_material": "cotton",
                                            "product_country": "Turkey",
                                            "product_off_percent": 20,
                                            "is_available": False
                                        })