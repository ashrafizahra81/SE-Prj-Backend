from .favorite_product_interface import FavoriteProductService, ShowFavoriteProductService, DeleteFromFavoriteProductsService
from ..models import UserFavoriteProduct
from Backend import dependencies
from rest_framework.response import Response
from rest_framework import status
from products.models import Product

import logging
logger = logging.getLogger("django")

class ConcreteFavoriteProductService(FavoriteProductService):

    def create_favorite_product(self, user, product):
        favorite_product = UserFavoriteProduct(
            user=user,
            product=product
        )
        favorite_product.save()

class ConcreteShowFavoriteProductService(ShowFavoriteProductService):

    def show_favorite_product(self, request):
        
        logger.info('request recieved from GET /favoriteProducts/show_favorite/')
        user_favorite_product = list(UserFavoriteProduct.objects.filter(user_id=request.user.id).values())
        product_list = list()
        for i in user_favorite_product:
            product_list.append(Product.objects.filter(id=i["product_id"]).values())
        data1 = list()
        if user_favorite_product:
            data1 = dependencies.show_favorite_products_service_instance.show_favorite_products(product_list)
            return Response(data1, status=status.HTTP_200_OK)

class ConcreteDeleteFromFavoriteProductsService(DeleteFromFavoriteProductsService):

    def delete_from_favorite_product(self, request):
        
        logger.info('request recieved from POST /favoriteProducts/delete_from_favorite/')
        deleted = UserFavoriteProduct.objects.filter(product_id=request.data['data']).delete()
        if(deleted[0] == 0):
            logger.warn('product with id ' +str(request.data['data'])+' has been deleted from product list')
            message = {"message": "محصول مورد نظر برای حذف یافت نشد"}
            return Response(status=status.HTTP_404_NOT_FOUND, data=message)
        logger.info('product with id '+str(request.data['data'])+' deleted from favorite list')
        message = {"message": "محصول مورد نظر با موفقیت از لیست علاقه مندی حذف شد"}
        return Response(status=status.HTTP_200_OK, data=message)


