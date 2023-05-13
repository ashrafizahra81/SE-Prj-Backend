from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *

class TestFavoriteProductsUrls(SimpleTestCase):

    def test_add_to_favorite_url(self):

        #Arrange
        add_to_favorite_url = reverse('add-to-favorite')

        #Assert
        self.assertEqual(resolve(add_to_favorite_url).func.view_class , AddToFavoriteProduct)
    
    def test_delete_from_favorite_url(self):
    
        #Arrange
        add_to_favorite_url = reverse('delete-from-favorite')

        #Assert
        self.assertEqual(resolve(add_to_favorite_url).func.view_class , DeleteFromFavoriteProducts)
    
    def test_show_favorite_url(self):
    
        #Arrange
        show_favorite_url = reverse('show-favorite')

        #Assert
        self.assertEqual(resolve(show_favorite_url).func.view_class , ShowFavoriteProduct)