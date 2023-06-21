from abc import ABC, abstractmethod

class ShopService(ABC):

    @abstractmethod
    def get_shop_info(self, user_id , products):
        pass
