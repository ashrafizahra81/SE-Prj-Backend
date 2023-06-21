from .shop_interface import *
class ConcreteShopService(ShopService):
    def get_shop_info(self, user_id , products):
        