from .shop_interface import *
class ConcreteShopService(ShopService):
    def get_shop_info(self, shop , products):
        data2 = {}
        data1 = []
        for i in products:
            data1.append(dict(i))
        data2["products"] = data1
        data2["shop_name"] = shop.shop_name
        data2["shop_address"] = shop.shop_address
        data2["shop_phone_number"] = shop.shop_phone_number
        return data2
    
    def calculate_total_price(self, product_list):
        totalPriceOfShop = 0
        for product in product_list:
            totalPriceOfShop = totalPriceOfShop + (product['initial_inventory'] - product['inventory']) * product['product_price']
        return totalPriceOfShop