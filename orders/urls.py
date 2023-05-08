from django.urls import path , include
from . import views



urlpatterns = [
    path('user_orders/', views.GetUserOrders.as_view(), name="get user orders"),
    path('checkout/', views.CheckoutShoppingCart.as_view(), name="checkout shopping cart"),
    path('show_order_to_shop/', views.ShowOrdersToShop.as_view(), name="show orders product"),
]