from abc import ABC, abstractmethod

class FavoriteProductService(ABC):

    @abstractmethod
    def create_favorite_product(self, user, product):
        pass
    
