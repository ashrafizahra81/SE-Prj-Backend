from abc import ABC, abstractmethod

class ShoppnigCartService(ABC):

    @abstractmethod
    def create_shopping_cart(self, user_id , product_id):
        pass

    @abstractmethod
    def calculate_checkout_info(self , user_id):
        pass