from .apply_discount_interface import ApplyDiscountService
from shoppingCarts.models import UserShoppingCart
from products.models import Product
from ..models import Gift
import logging
logger = logging.getLogger("django")



class ConcreteApplyDiscountService(ApplyDiscountService):

    def cal_total_price_of_shopping_cart(self, user_cart):
        off_price = 0
        for o1 in user_cart:
            product1 = Product.objects.get(pk=o1['product_id'])
            off_price += ((100 - product1.product_off_percent) / 100) * product1.product_price
        logger.info('total price of shopping cart calculated: '+str(off_price))
        
        return off_price
    def check_gift_type(self, discount_code, off_price):
        gift = Gift.objects.get(discount_code = discount_code)
        data = {}
        if(gift.type =='C'):
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = off_price
            logger.info('The discount code applied and total price of shopping cart changed to '+str(data['discounted_total_cost']))
        elif(gift.type == 'A'):
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = (0.8) * (off_price+30000)
            logger.info('The discount code applied and total price of shopping cart changed to '+str(data['discounted_total_cost']))

        else:
            data["total_cost"] = off_price+30000
            data["discounted_total_cost"] = (0.7) * (off_price+30000)
            logger.info('The discount code applied and total price of shopping cart changed to '+str(data['discounted_total_cost']))

        data['shippingPrice'] = 30000

        return data