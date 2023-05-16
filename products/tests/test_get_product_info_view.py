from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestGetProductInfo(APITestCase):

    fixtures = ['accounts', 'products']
    get_product_info_url = reverse('product-info', kwargs={'pk': 1})

    def test_get_existing_product_info(self):
        
        response = self.client.get(self.get_product_info_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data,{
                                            "id": 1,
                                            "product_name": "T-shirt",
                                            "product_price": 120000,
                                            "upload": "/null",
                                            "inventory": 5,
                                            "initial_inventory": 12,
                                            "product_size": "38",
                                            "product_group": "T-shirt",
                                            "product_image": "https://s28.picofile.com/file/8462477276/u1ktrbrvf0_rvca_f_4409_frt1.jpg",
                                            "product_color": "multi color",
                                            "product_height": 20,
                                            "product_design": "striped",
                                            "product_material": "cotton",
                                            "product_country": "Iran",
                                            "product_off_percent": 0,
                                            "is_available": True,
                                            "is_deleted": False,
                                            "score": 0,
                                            "number_of_votes": 0,
                                            "last_product_sold_date": "2023-05-14T20:40:01.126548Z",
                                            "shop": 4,
                                            "is_favorite": False,
                                            "is_in_cart": False
                                        })
    
    def test_get_non_existing_product_info(self):

        self.get_product_info_url = reverse('product-info', kwargs={'pk': 2})
        response = self.client.get(self.get_product_info_url, kwargs={'pk': 2}, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
    
