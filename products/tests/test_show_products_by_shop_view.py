from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestShowProductsByShop(APITestCase):

    fixtures = ['accounts', 'products']
    show_products_to_shop_urls = reverse('show-products-of-shop')

    def setUp(self):

        self.user = User.objects.get(id=4)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))


    def test_show_products_of_shop_should_succeed_when_to_a_shop_manager(self):

        response = self.client.get(self.show_products_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, {
                "products": [
                    {
                        "id": 1,
                        "product_name": "T-shirt",
                        "product_price": 120000,
                        "product_off_percent": 0,
                        "inventory": 5,
                        "upload": "https://s28.picofile.com/file/8462477276/u1ktrbrvf0_rvca_f_4409_frt1.jpg",
                        "shop_id": 4
                    },
                    {
                        "id": 3,
                        "product_name": "pants",
                        "product_price": 620000,
                        "product_off_percent": 0,
                        "inventory": 15,
                        "upload": "https://s29.picofile.com/file/8462060092/images.jpg",
                        "shop_id": 4
                    },
                    {
                        "id": 4,
                        "product_name": "pants",
                        "product_price": 400000,
                        "product_off_percent": 0,
                        "inventory": 18,
                        "upload": "https://s28.picofile.com/file/8462477126/DSC_7010_91576.jpg",
                        "shop_id": 4
                    },
                    {
                        "id": 5,
                        "product_name": "T-shirt",
                        "product_price": 110000,
                        "product_off_percent": 0,
                        "inventory": 19,
                        "upload": "https://s28.picofile.com/file/8462477268/contentsArea_itemimg_16.jpg",
                        "shop_id": 4
                    }
                ],
                "shop_name": "shop1",
                "shop_address": "isfahan",
                "shop_phone_number": "09808949238"
                                            })

    def test_show_products_of_shop_should_raise_error_when_to_a_customer_not_a_shop_manager(self): 

            self.user = User.objects.get(id=2)
            self.access_token = AccessToken.for_user(self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

            response = self.client.get(self.show_products_to_shop_urls, format = 'json')
            self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data, {
                                                "detail": "You do not have permission to perform this action."
                                            })


    def test_show_products_should_raise_error_when_without_authentication(self):

            self.client.force_authenticate(user=None , token = None)
            response = self.client.get(self.show_products_to_shop_urls, format = 'json')
            self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
        
    def test_show_products_with_off_percent_should_succeed_when_to_a_shop_manager(self):

        self.user = User.objects.get(id=5)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

        response = self.client.get(self.show_products_to_shop_urls, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data, {
                "products": [
                    {
                    "id": 6,
                    "product_name": "T-shirt",
                    "product_price": 110000,
                    "product_off_percent": 88000.0,
                    "inventory": 17,
                    "upload": "https://s28.picofile.com/file/8462477250/contentsArea_itemimg_15.jpg",
                    "shop_id": 5
                },
                    {
                        "id": 7,
                        "product_name": "T-shirt",
                        "product_price": 110000,
                        "product_off_percent": 0,
                        "inventory": 20,
                        "upload": "https://s29.picofile.com/file/8462477242/91R2DALbF9L_AC_UL1500_.jpg",
                        "shop_id": 5
                    },
                    {
                        "id": 8,
                        "product_name": "pants",
                        "product_price": 550000,
                        "product_off_percent": 0,
                        "inventory": 0,
                        "upload": "https://s28.picofile.com/file/8462477118/8228022250_6_1_1.jpg",
                        "shop_id": 5
                    },
                    {
                        "id": 9,
                        "product_name": "hoodie",
                        "product_price": 2650000,
                        "product_off_percent": 0,
                        "inventory": 14,
                        "upload": "https://s29.picofile.com/file/8462477634/51MiK2fjBtL_AC_SX679_.jpg",
                        "shop_id": 5
                    }
                ],
                "shop_name": "shop2",
                "shop_address": "isfahan",
                "shop_phone_number": "09808949000"
            }
        )