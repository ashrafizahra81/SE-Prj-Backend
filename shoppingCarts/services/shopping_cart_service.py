from .shopping_cart_interface import UserShoppnigCart
from shoppingCarts.models import UserShoppingCart

class GetShoppingCartByUserId(UserShoppnigCart):
    def get_user_shopping_cart(self, user_id):
       return list(UserShoppingCart.objects.filter(user_id=user_id).values())
