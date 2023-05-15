from rest_framework.permissions import BasePermission 
class IsShopOwner(BasePermission):
    message = 'permission denied, you are not shop owner'
    def has_permission(self, request, view):
        if(request.user.is_authenticated and request.user):
            if(request.user.shop_name != None):
                return True
            return False
        return False
    
    def has_object_permission(self, request, view, obj):
        print(request.user.shop_name)
        return request.user.shop_name != None