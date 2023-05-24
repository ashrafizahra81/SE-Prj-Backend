from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestAddProductToShop(APITestCase):

    fixtures = ['accounts', 'products']
    add_product_to_shop_urls = reverse('add-products-to-shop')

    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_add_product_to_shop_by_a_shop_manager(self):
        
        data = {
                "product_name": "pants",
                "product_price": "2330000",
                "product_size": "38",
                "product_group": "pants",
                "product_image": "https://s29.picofile.com/file/8462477084/2.jpg",
                "product_color": "light blue",
                "product_height": "85",
                "product_design": "plain",
                "product_material": "linen",
                "product_country": "Iran",
                "inventory": "10"
                }
        
        response = self.client.post(self.add_product_to_shop_urls, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
                                            "product_id": 17,
                                            "product_name": "pants",
                                            "product_price": "2330000",
                                            "product_size": "38",
                                            "product_group": "pants",
                                            "product_image": "https://s29.picofile.com/file/8462477084/2.jpg",
                                            "product_color": "light blue",
                                            "product_height": "85",
                                            "product_design": "plain",
                                            "product_material": "linen",
                                            "product_country": "Iran",
                                            "inventory": "10"
                                        })

    def test_add_product_to_shop_by_a_user_who_is_not_a_shop_manager(self):

        self.user = User.objects.get(id=2)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        
        data = {
                "product_name": "pants",
                "product_price": "2330000",
                "product_size": "38",
                "product_group": "pants",
                "product_image": "https://s29.picofile.com/file/8462477084/2.jpg",
                "product_color": "light blue",
                "product_height": "85",
                "product_design": "plain",
                "product_material": "linen",
                "product_country": "Iran",
                "inventory": "10"
                }
        response = self.client.post(self.add_product_to_shop_urls, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
                                            "detail": "You do not have permission to perform this action."
                                        })

    

    def test_add_product_to_shop_without_authentication(self):

        self.client.force_authenticate(user=None , token = None)
        data = {
                "product_name": "pants",
                "product_price": "2330000",
                "product_size": "38",
                "product_group": "pants",
                "product_image": "https://s29.picofile.com/file/8462477084/2.jpg",
                "product_color": "light blue",
                "product_height": "85",
                "product_design": "plain",
                "product_material": "linen",
                "product_country": "Iran",
                "inventory": "10"
                }
        response = self.client.post(self.add_product_to_shop_urls, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
    
    def test_add_product_to_shop_by_a_shop_manager_and_invalid_data(self):

        data = {
                "product_name": "pants",
                "product_price": "2330000",
                "product_size": "38",
                "product_group": "pants",
                "product_image": "https://s29.picofile.com/file/8462477084/2.jpg",
                "product_color": "light blue",
                "product_height": "85 meters",
                "product_design": "plain",
                "product_material": "linen",
                "product_country": "Iran",
                "inventory": "10"
                }
        
        response = self.client.post(self.add_product_to_shop_urls, data,  format = 'json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)