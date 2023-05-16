from django.urls import path , include
from . import views



urlpatterns = [
    path('show_gift/', views.ShowGiftInfo.as_view(), name='show_gift'),
    path('get_gift/', views.GetGift.as_view(), name='get_gift'),
    path('apply_discount/', views.ApplyDiscount.as_view(), name='apply_discount'),
]