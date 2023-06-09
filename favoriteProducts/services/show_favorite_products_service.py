from .show_favorite_products_interface import ShowFavoriteProductService
import logging
logger = logging.getLogger("django")

class ConcreteShowFavoriteProductService(ShowFavoriteProductService):

    def show_favorite_products(self, product_list):
        
        data = {}
        data1 = list()
        for i in product_list:
            if i[0]['is_deleted'] == False:
                logger.info('product with id ' +str(i[0]['id'])+' from favorite list found')
                data = {}
                data['id'] = i[0]['id']
                data['product_name'] = i[0]['product_name']
                data['product_price'] = i[0]['product_price']
                price_off = 0
                if int(i[0]['product_off_percent']) > 0:
                    price_off = ((100 - int(i[0]['product_off_percent'])) / 100) * int(i[0]['product_price'])
                data['product_off_percent'] = price_off
                data['upload'] = i[0]['upload']
                data1.append(data)
                logger.warn('product with id ' +str(i[0]['id'])+' has been deleted from product list')
        
        return data1
            
        