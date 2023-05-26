from django.urls import path , include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegister.as_view(),name='register'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('edit_profile/', views.UserEditProfile.as_view(), name="edit-profile"),
    path('create_shop/', views.ShopManagerRegister.as_view(), name="create_shop"),
    path('edit_shop/', views.EditShop.as_view(), name="edit_shop"),
    path('show_user_info/', views.ShowUserInfo.as_view(), name="show_user_info"),
    path('api/token/verify/', views.TokenVerifyView.as_view(), name='token_verify'),
    path('show_score/', views.show_score.as_view(), name='show_score'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('receive_email_for_recover_password/', views.ReceiveEmailForRecoverPassword.as_view(), name='receive_email'),
    # path('recover_password/<int:pk>/', views.RecoverPassword.as_view(), name="recover_password"),
    path('verify_email/', views.verfyUserToResgister.as_view(), name='verify_email'),
]
