from .orders_interface import *
from ..models import Order
from products.serializers import ProductsSerializer , EditProductSerializer
from products.models import Product
from datetime import datetime
from Backend import dependencies
import logging
from wallets.models import Wallet
from shoppingCarts.models import UserShoppingCart
from products.serializers import *
logger = logging.getLogger("django")

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
    
    def calculate_price(self, user_cart):
        price = 0
        off_price = 0
        for o1 in user_cart:
            product = Product.objects.get(pk=o1['product_id'])
            dependencies.purchaseService_instance.decrease_number_of_product(product)
            off_price += ((100 - product.product_off_percent) / 100) * product.product_price
            price += product.product_price
        return price , off_price
    

    def check_type_of_payment(self, user_id, payment_type , price):
        wallet = Wallet.objects.get(user_id = user_id)
        balance = wallet.balance
        if(payment_type =="wallet"):
            logger.info('balance of wallet is '+str(wallet.balance))
            balance = dependencies.purchaseService_instance.buy_from_wallet(wallet , price+30000)
            if balance != None:
                logger.info('balance of wallet reduced to '+str(balance))
                return balance

            else:
                logger.warn('wallet balance of user '+str(user_id)+ ' is not enough')
                return -1
        return balance
        


    def purchase(self, user, user_cart, price, off_price, balance):
        for o in user_cart:
            product = Product.objects.get(pk=o['product_id'])
            if product.is_deleted == False:
                dependencies.cerate_order_service_instance.createOrder(user , product, product.product_price ,price+30000 ,off_price+30000,"Accepted")
            UserShoppingCart.objects.filter(user_id=user.id).delete()
        logger.info('order of user '+str(user.id)+' saved successfuly')
        dependencies.user_service_instance.updateUserScore(off_price / 100000 , user)
        logger.info('score of this shop added to scores of user ' +str(user.id))            
        data = {}
        data["message"] = "خرید با موفقیت انجام شد"
        data["balance"] = balance
        return data
    
class ConcreteCreateOrder(CreateOrderService):
    def createOrder(self, user, product, cost, total_cost, off_cost, status):
        c = Order(
                    user=user,
                    product=product,
                    cost=cost,
                    total_cost=total_cost,
                    off_cost=off_cost,
                    status=status,
                )
        c.save()    


class ConcreteShopOrderService(ShopOrderServiceInterface):
    def show_orders_to_shop(self, order_list , request):
        product_list = list()
        for order in order_list:
            for product in Product.objects.all().values():
                if product['id'] == order['product_id']:
                    if product['shop_id'] == request.user.id:
                        data = ProductsOfOrderSerializer(product)
                        product_list.append(data.data)
        return product_list