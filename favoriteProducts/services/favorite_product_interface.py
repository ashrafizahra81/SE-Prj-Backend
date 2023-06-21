from abc import ABC, abstractmethod

class FavoriteProductService(ABC):

    @abstractmethod
    def create_favorite_product(self, user, product):
        pass
    
class ShowFavoriteProductService(ABC):

    def show_favorite_product(self, request):
        pass

class DeleteFromFavoriteProductsService(ABC):

    @abstractmethod
    def delete_from_favorite_product(self, request):
        pass