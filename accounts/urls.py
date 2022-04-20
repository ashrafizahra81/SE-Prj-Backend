from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegister.as_view() , name="register"),
    path('login/', obtain_auth_token , name = "login"),
]
