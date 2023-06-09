from rest_framework.test import APITestCase, APIClient
from ..views import *
from django.urls import path, reverse, include, resolve
from accounts.models import User
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

class TestShowAllProducts(APITestCase):

    fixtures = ['accounts', 'products']
    show_all_products_url = reverse('show-all-products')

    def test_show_all_products_should_succeed_when_the_user_has_been_authorized_or_not(self):

        response = self.client.get(self.show_all_products_url, format = 'json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data, [
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
                },
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
                },
                {
                    "id": 10,
                    "product_name": "hoodie",
                    "product_price": 2680000,
                    "product_off_percent": 0,
                    "inventory": 17,
                    "upload": "https://s29.picofile.com/file/8462477642/444e6c91e98755746526021917ce48ff.jpg",
                    "shop_id": 6
                },
                {
                    "id": 11,
                    "product_name": "T-shirt",
                    "product_price": 1180000,
                    "product_off_percent": 0,
                    "inventory": 17,
                    "upload": "https://s29.picofile.com/file/8462477226/41W7kdlxcES_AC_UX466_.jpg",
                    "shop_id": 6
                },
                {
                    "id": 12,
                    "product_name": "hoodie",
                    "product_price": 2180000,
                    "product_off_percent": 0,
                    "inventory": 17,
                    "upload": "https://s29.picofile.com/file/8462477618/4.jpg",
                    "shop_id": 6
                },
                {
                    "id": 13,
                    "product_name": "pants",
                    "product_price": 3180000,
                    "product_off_percent": 0,
                    "inventory": 1,
                    "upload": "https://s29.picofile.com/file/8462477084/2.jpg",
                    "shop_id": 6
                },
                {
                    "id": 14,
                    "product_name": "pants",
                    "product_price": 3880000,
                    "product_off_percent": 0,
                    "inventory": 10,
                    "upload": "https://s28.picofile.com/file/8462477076/1.jpg",
                    "shop_id": 6
                }
            ]
        )