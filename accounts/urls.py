from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'accounts'

AddProductsToShop_list = views.AddProductsToShopViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('register/', views.UserRegister.as_view()),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('edit_profile/<int:pk>/', views.UserEditProfile.as_view(), name="edit profile"),
    path('user_styles/', views.UserStyles.as_view(), name="user styles"),
    path('add_to_cart/', views.AddToShoppingCartView.as_view(), name="add to cart"),
    path('delete_from_cart/', views.DeleteFromShoppingCart.as_view(), name="delete from cart"),
    path('show_cart/', views.ShowUserShoppingCart.as_view(), name="show-cart"),
    path('add_to_favorite/', views.AddToFavoriteProduct.as_view(), name="add-to-favorite"),
    path('show_favorite/', views.ShowFavoriteProduct.as_view(), name="show-favorite"),
    path('delete_from_favorite/', views.DeleteFromFavoriteProducts.as_view(), name="delete-from-favorite"),
    path('add_products_to_shop/', AddProductsToShop_list, name="add products to shop"),
    path('create_shop/', views.ShopManagerRegister.as_view(), name="create shop"),
    path('edit_shop/<int:pk>/', views.EditShop.as_view(), name="edit shop"),
    path('edit_product/<int:pk>/', views.EditProduct.as_view(), name="edit product"),
    path('delete_product/<int:pk>/', views.DeleteProduct.as_view(), name="delete product"),
    path('product_info/<int:pk>/', views.GetProductInfo.as_view(), name="get product info"),
    path('user_orders/', views.GetUserOrders.as_view(), name="get user orders"),
    path('checkout/', views.CheckoutShoppingCart.as_view(), name="checkout shopping cart"),
    path('show_products_of_shop/', views.ShowProductsByShop.as_view(), name="show shops' product"),
    path('show_order_to_shop/', views.ShowOrdersToShop.as_view(), name="show orders product"),

]
