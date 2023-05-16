from django.urls import path , include
from . import views



urlpatterns = [
    path('user_orders/', views.GetUserOrders.as_view(), name="user-orders"),
    path('checkout/', views.CheckoutShoppingCart.as_view(), name="checkout"),
    path('show_order_to_shop/', views.ShowOrdersToShop.as_view(), name="show-order-to-shop"),
]