from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *


class TestOrdersUrls(SimpleTestCase):

    def test_get_orders_url(self):

        get_orders_url = reverse('user-orders')
        self.assertEqual(resolve(get_orders_url).func.view_class , GetUserOrders)
    
    def test_checkout_urls(self):

        checkout_urls = reverse('checkout')
        self.assertEqual(resolve(checkout_urls).func.view_class , CheckoutShoppingCart)
    
    def test_show_orders_to_shop_urls(self):

        show_orders_to_shop_urls = reverse('show-order-to-shop')
        self.assertEqual(resolve(show_orders_to_shop_urls).func.view_class , ShowOrdersToShop)