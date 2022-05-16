from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'accounts'


# createShopManagerRegister_list = views.ShopManagerRegisterViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

AddProductsToShop_list = views.AddProductsToShopViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
#

urlpatterns = [
    path('register/', views.UserRegister.as_view()),
    # path('shop_manager_register/', views.ShopManagerRegister.as_view()),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('edit_profile/<int:pk>/', views.UserEditProfile.as_view(), name="edit profile"),
    path('user_styles/', views.UserStyles.as_view(), name="user styles"),
    path('user_shops/<int:pk>/', views.ShopsForUser.as_view(), name="shops for user"),
    path('add_products_to_shop/', AddProductsToShop_list, name="add products to shop"),
    # path('create_shop/', createShopManagerRegister_list, name="create shop"),
    path('create_shop/', views.ShopManagerRegister.as_view(), name="create shop"),
    path('edit_shop/<int:pk>/', views.EditShop.as_view(), name="edit shop"),
    path('edit_product/<int:pk>/', views.EditProduct.as_view(), name="edit product"),
    path('delete_product/<int:pk>/', views.DeleteProduct.as_view(), name="delete product"),
    path('checkout/', views.CheckoutShoppingCart.as_view(), name="checkout shopping cart"),

]

