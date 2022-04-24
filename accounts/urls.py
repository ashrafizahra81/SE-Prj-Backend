from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegister.as_view()),
    path('login/', obtain_auth_token, name="login"),
    path('edit_profile/<int:pk>/', views.UserEditProfile.as_view(), name="edit profile"),
    path('user_styles/<int:pk>/', views.UserStyles.as_view(), name="user styles"),
    path('user_shops/<int:pk>/', views.ShopsForUser.as_view(), name="shops for user"),

]
