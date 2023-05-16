from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *

class TestGiftsUrls(SimpleTestCase):

    def test_show_gift_url(self):

        #Arrange
        show_gift_url = reverse('show_gift')

        #Assert
        self.assertEqual(resolve(show_gift_url).func.view_class , ShowGiftInfo)
    
    def test_get_gift_url(self):
    
        #Arrange
        get_gift_url = reverse('get_gift')

        #Assert
        self.assertEqual(resolve(get_gift_url).func.view_class , GetGift)
    
    def test_apply_discount_url(self):
    
        #Arrange
        apply_dicount_url = reverse('apply_discount')

        #Assert
        self.assertEqual(resolve(apply_dicount_url).func.view_class , ApplyDiscount)