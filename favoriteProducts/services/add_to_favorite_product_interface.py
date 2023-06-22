from abc import ABC, abstractmethod

class AddToFavoriteProductService(ABC):

    @abstractmethod
    def add_to_favorite_product(self, request):
        pass