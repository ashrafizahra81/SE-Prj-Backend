from .product_interfaces import *
from ..models import Product
from ..serializers import *
import logging
from ..serializers import *
logger = logging.getLogger("django")


class ConcreteUpdateProductForDeletedProduct(UpdateProductService):

    def update_product(self, product_id , request):
        product = Product.objects.get(pk=product_id)
        product.is_deleted = True
        product.save()

class ConcreteUpdateProductByEditing(UpdateProductService):

    def update_product(self, product_id, request):
        product = Product.objects.get(pk = product_id)
        serialized_data = EditProductSerializer(instance=product, data=request, partial=True)
        if serialized_data.is_valid():
            logger.info('Data entered is valid')
            serialized_data.save()
            return True
        return serialized_data.errors
    

class ConcreteCreateProduct(CreateProductService):
    def create_product(self, product_info , user_id):
        if(type(product_info) != dict):
            data = product_info.dict()
        else :
            data = product_info
        data['shop']=user_id
        data['is_available']=1
        data['initial_inventory']=product_info['inventory']
        _serializer = SaveProductsSerializer(data=data)
        if _serializer.is_valid():
            logger.info('data entered is valid')
            product = _serializer.save()
            logger.info('product with id '+str(product.id)+' saved')
            return [True , ProductsSerializer(product)]
        return [False ,_serializer.errors]
    

class ConcreteFilterProduct(FilterProductService):
    def filter_product(self, filter):
        data=[]
        if filter == "pants" or filter == "T-shirt" or filter == "shirt" or filter == "hoodie":
            products = list(Product.objects.filter(product_group=filter).values())
            data = FilterSerializer(products , many = True).data  
            data1 = []
            for i in data:
                data1.append(dict(i)) 
        return data1
        
        