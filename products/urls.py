from django.urls import path , include
from . import views

AddProductsToShop_list = views.AddProductsToShopViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = [
    path('edit_product/<int:pk>/', views.EditProduct.as_view(), name="edit product"),
    path('delete_product/<int:pk>/', views.DeleteProduct.as_view(), name="delete-product"),
    path('product_info/<int:pk>/', views.GetProductInfo.as_view(), name="product-info"),
    path('add_products_to_shop/', AddProductsToShop_list, name="add-products-to-shop"),
    path('show_products_of_shop/', views.ShowProductsByShop.as_view(), name="show-products-of-shop"),
    path('show_all_products/', views.ShowAllProducts.as_view(), name="show-all-products"),
    path('report/', views.Report.as_view(), name='report'),
    path('filters/', views.Filters.as_view(), name='filters'),
]