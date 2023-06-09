from abc import ABC, abstractmethod

class ApplyDiscountService(ABC):

    @abstractmethod
    def cal_total_price_of_shopping_cart(self, user_cart):
        pass

    @abstractmethod
    def check_gift_type(self, discount_code, data):
        pass