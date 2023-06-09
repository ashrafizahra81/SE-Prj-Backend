from abc import ABC, abstractmethod

class ShowFavoriteProductService(ABC):

    @abstractmethod
    def show_favorite_products(self, product_list):
        pass