from .add_to_favorite_product_interface import AddToFavoriteProductService
from products.models import Product
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status

import logging
logger = logging.getLogger("django")


class ConcreteAddToFavoriteProductService(AddToFavoriteProductService):

    def add_to_favorite_product(self, request):
        logger.info('request recieved from POST /favoriteProducts/add_to_favorite/')
        message = ""
        for product in Product.objects.all():
            
            if product.pk == int(request.data['data']):
                dependencies.favorite_product_service_instance.create_favorite_product(request.user, product)
                logger.info('product '+str(product.pk)+' added to favorite list of user '+str(request.user.pk))
                message = {"message": "محصول مورد نظر به لیست علاقه مندی ها اضافه شد"}
                return Response(status=status.HTTP_200_OK, data=message)
        logger.warn('product with id'+str(product.pk)+' not found')
        message = {"message": "محصول مورد نظر در لیست محصولات نیست"}
        return Response(status=status.HTTP_404_NOT_FOUND, data=message)