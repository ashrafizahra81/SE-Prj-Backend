from abc import ABC, abstractmethod

class ShopService(ABC):

    @abstractmethod
    def get_shop_info(self, shop , products):
        pass
    
    @abstractmethod
    def calculate_total_price(self , product_list):
        pass