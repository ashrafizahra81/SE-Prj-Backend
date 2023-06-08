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

class CreateOrderService(ABC):
    @abstractmethod
    def createOrder(self, user, product,cost,total_cost,off_cost,status):
        pass