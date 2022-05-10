from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegister.as_view()),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('edit_profile/<int:pk>/', views.UserEditProfile.as_view(), name="edit profile"),
    path('user_styles/', views.UserStyles.as_view(), name="user styles"),
    path('user_shops/<int:pk>/', views.ShopsForUser.as_view(), name="shops for user"),
    path('add_to_cart/', views.AddToShoppingCartView.as_view(), name="add to cart"),
    path('delete_from_cart/', views.DeleteFromShoppingCart.as_view(), name="delete from cart"),
]
