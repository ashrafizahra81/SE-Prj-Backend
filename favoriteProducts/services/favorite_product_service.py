from .favorite_product_interface import FavoriteProductService
from ..models import UserFavoriteProduct

class ConcreteFavoriteProductService(FavoriteProductService):

    def create_favorite_product(self, user, product):
        favorite_product = UserFavoriteProduct(
            user=user,
            product=product
        )
        favorite_product.save()