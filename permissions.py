from rest_framework.permissions import BasePermission , SAFE_METHODS

class IsShopOwner(BasePermission):
    message = 'permission denied, you are not shop owner'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.shop == request.user

class IsShopManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return request.user.shop_name != None 
