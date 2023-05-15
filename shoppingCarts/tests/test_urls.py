from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *

class TestShoppingCartsUrls(SimpleTestCase):

    def test_add_to_cart_url(self):

        add_to_cart_url = reverse('add-to-cart')
        self.assertEqual(resolve(add_to_cart_url).func.view_class , AddToShoppingCartView)
    
    def test_delete_from_cart_url(self):

        delete_from_cart_url = reverse('delete-from-cart')
        self.assertEqual(resolve(delete_from_cart_url).func.view_class , DeleteFromShoppingCart)
    
    def test_show_user_cart_url(self):

        show_user_cart_url = reverse('show-cart')
        self.assertEqual(resolve(show_user_cart_url).func.view_class , ShowUserShoppingCart)
    
    def test_show_checkout_info_url(self):

        show_checkout_info_url = reverse('show-checkout-info')
        self.assertEqual(resolve(show_checkout_info_url).func.view_class , show_checkout_info)