from django.urls import path , include
from . import views



urlpatterns = [
    path('add_to_cart/', views.AddToShoppingCartView.as_view(), name="add to cart"),
    path('delete_from_cart/', views.DeleteFromShoppingCart.as_view(), name="delete from cart"),
    path('show_cart/', views.ShowUserShoppingCart.as_view(), name="show-cart"),
    path('show_checkout_info/', views.show_checkout_info.as_view(), name='checkout_info'),
]