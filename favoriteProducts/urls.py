from django.urls import path , include
from . import views



urlpatterns = [
    path('add_to_favorite/', views.AddToFavoriteProduct.as_view(), name="add-to-favorite"),
    path('show_favorite/', views.ShowFavoriteProduct.as_view(), name="show-favorite"),
    path('delete_from_favorite/', views.DeleteFromFavoriteProducts.as_view(), name="delete-from-favorite"),
]