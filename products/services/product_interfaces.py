from abc import ABC, abstractmethod

class UpdateProductService(ABC):

    @abstractmethod
    def update_product(self, product_id , request):
        pass
    
class CreateProductService(ABC):
    @abstractmethod
    def create_product(self , product_info, user_id):
        pass
class FilterProductService(ABC):
    @abstractmethod
    def filter_product(self , filter):
        pass