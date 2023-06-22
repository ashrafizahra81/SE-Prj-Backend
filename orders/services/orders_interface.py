from abc import ABC, abstractmethod

class UserOrderServiceInterface(ABC):

    @abstractmethod
    def get_user_orders(self, user_id):
        pass
    

class PurchaseInterface(ABC):
    @abstractmethod
    def decrease_number_of_product(self , product):
        pass

    @abstractmethod
    def buy_from_wallet(self, wallet, price):
        pass
    @abstractmethod
    def calculate_price(self, user_cart):
        pass

    @abstractmethod
    def check_type_of_payment(self, user_id, payment_type,price):
        pass

    @abstractmethod
    def purchase(self, user, user_cart, price, off_price, balance):
        pass

class CreateOrderService(ABC):
    @abstractmethod
    def createOrder(self, user, product,cost,total_cost,off_cost,status):
        pass


class ShopOrderServiceInterface(ABC):
    @abstractmethod
    def show_orders_to_shop(self, order_list , request):
        pass