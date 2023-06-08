from abc import ABC, abstractmethod

class UserShoppnigCart(ABC):
    @abstractmethod
    def get_user_shopping_cart(self, user_id):
        pass