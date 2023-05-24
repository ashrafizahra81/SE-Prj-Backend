from django.urls import path , include
from . import views



urlpatterns = [
    path('charge_wallet/', views.ChargeWallet.as_view() , name='charge_wallet'),
    # path('buy_from_wallet/', views.BuyFromWallet.as_view()),
]