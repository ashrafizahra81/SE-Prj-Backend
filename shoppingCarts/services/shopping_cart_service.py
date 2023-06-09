from .shopping_cart_interface import ShoppnigCartService
from shoppingCarts.models import UserShoppingCart
from products.models import Product

class ConcreteShoppingCart(ShoppnigCartService):

    def create_shopping_cart(self, user_id, product_id):
        if(Product.objects.filter(id=product_id).exists()):
            product = Product.objects.get(id = product_id)
            if product.inventory > 0:
                cart = UserShoppingCart(
                    user=user_id,
                    product=product
                )
                cart.save()
            return True
        return False
    
    def calculate_checkout_info(self, user_id):
        user_cart = list(UserShoppingCart.objects.filter(user_id=user_id).values())
        off_price = 0
        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            if(product1.is_deleted == 1 or product1.is_available == 0):
                return False
            off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
        data={}
        data["discounted_price"] = off_price
        data["total_cost"] = off_price+30000
        data["score"] = int((off_price+30000)/100000)
        data["shippingPrice"] = 30000
        return data
        