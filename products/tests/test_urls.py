from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *

class TestFiltersUrls(SimpleTestCase):
    
    def test_delete_product(self):

        delete_product_url = reverse('delete-product',  kwargs={'pk': 1})
        self.assertEqual(resolve(delete_product_url).func.view_class,  DeleteProduct)

    def test_edit_product(self):

        edit_product_url = reverse('edit-product',  kwargs={'pk': 4})
        self.assertEqual(resolve(edit_product_url).func.view_class,  EditProduct)
    
    def test_get_product_info(self):

        get_product_info_url = reverse('product-info', kwargs={'pk': 1})
        self.assertEqual(resolve(get_product_info_url).func.view_class,  GetProductInfo)

    def test_show_products_by_shop(self):

        show_products_to_shop_urls = reverse('show-products-of-shop')
        self.assertEqual(resolve(show_products_to_shop_urls).func.view_class,  ShowProductsByShop)

    def test_show_all_products(self):

        show_all_products_url = reverse('show-all-products')
        self.assertEqual(resolve(show_all_products_url).func.view_class,  ShowAllProducts)

    def test_report(self):

        report_url = reverse('report')
        self.assertEqual(resolve(report_url).func.view_class,  Report)

    def test_filters(self):
        filters_url = reverse('filters')
        self.assertEqual(resolve(filters_url).func.view_class,  Filters)