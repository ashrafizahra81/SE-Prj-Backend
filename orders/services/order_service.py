from .orders_interface import UserOrderServiceInterface , PurchaseInterface
from ..models import Order
from products.serializers import ProductsSerializer , EditProductSerializer
from products.models import Product
from datetime import datetime

class UserOrderService(UserOrderServiceInterface):

    def get_user_orders(self, user_id):
        user_orders = list(Order.objects.filter(user_id = user_id).values())
        data = list()
        for order in user_orders:
            product = Product.objects.get(pk=order['product_id'])
            serialized_product = ProductsSerializer(instance=product)
            js = serialized_product.data
            js['cost'] = order['cost']
            js['status'] = order['status']
            data.append(js)
        return data
    



class Purchase(PurchaseInterface):

    def decrease_number_of_product(self, product):
        data = {}
        product_inventory = product.inventory - 1
        product.last_product_sold_date = datetime.today()
        if(product.inventory==0):
            product.is_available = 0
        data['inventory'] = product_inventory
        serialized_data = EditProductSerializer(instance=product, data=data, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()

    def buy_from_wallet(self, wallet, price):
        if(wallet.balance >= price):
            wallet.balance = wallet.balance - price
            wallet.save()
            return wallet.balance
        return None
        
    

