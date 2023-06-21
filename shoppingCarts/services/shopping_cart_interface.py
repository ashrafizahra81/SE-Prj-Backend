from abc import ABC, abstractmethod

class ShoppnigCartService(ABC):

    @abstractmethod
    def create_shopping_cart(self, user_id , product_id):
        pass

    @abstractmethod
    def calculate_checkout_info(self , user_id):
        pass

    @abstractmethod
    def calculate_shopping_cart_info(self , products):
        pass

    @abstractmethod
    def get_products_of_shop(self , user_id):
        pass