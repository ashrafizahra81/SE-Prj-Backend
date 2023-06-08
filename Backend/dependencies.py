from Backend import settings
import importlib

userOrderService_name = settings.ORDER_SERVICE
userOrderService_class = getattr(importlib.import_module(userOrderService_name.rsplit('.', 1)[0]), userOrderService_name.rsplit('.', 1)[1])
userOrderService_instance = userOrderService_class()

userCartService_name = settings.GET_USER_SHOPPING_CART_SERVICE
userCartService_class = getattr(importlib.import_module(userCartService_name.rsplit('.', 1)[0]), userCartService_name.rsplit('.', 1)[1])
userCartService_instance = userCartService_class()

purchaseService_name = settings.PURCHASE_SERVICE
purchaseService_class = getattr(importlib.import_module(purchaseService_name.rsplit('.', 1)[0]), purchaseService_name.rsplit('.', 1)[1])
purchaseService_instance = purchaseService_class()

mail_service_class_name = settings.MAIL_SERVICE
mail_service_class = getattr(importlib.import_module(mail_service_class_name.rsplit('.', 1)[0]), mail_service_class_name.rsplit('.', 1)[1])
mail_service_instance = mail_service_class()

uniqueCode_service_class_name = settings.UNIQUECODE_SERVICE
uniqueCode_service_class = getattr(importlib.import_module(uniqueCode_service_class_name.rsplit('.', 1)[0]), uniqueCode_service_class_name.rsplit('.', 1)[1])
uniqueCode_service_instance = uniqueCode_service_class()

codeForUsers_service_class_name = settings.CODEFORUSERS_SERVICE
codeForUsers_service_class = getattr(importlib.import_module(codeForUsers_service_class_name.rsplit('.', 1)[0]), codeForUsers_service_class_name.rsplit('.', 1)[1])
codeForUsers_service_instance = codeForUsers_service_class()

user_service_class_name = settings.USER_SERVICE
user_service_class = getattr(importlib.import_module(user_service_class_name.rsplit('.', 1)[0]), user_service_class_name.rsplit('.', 1)[1])
user_service_instance = user_service_class()

wallet_service_class_name = settings.WALLET_SERVICE
wallet_service_class = getattr(importlib.import_module(wallet_service_class_name.rsplit('.', 1)[0]), wallet_service_class_name.rsplit('.', 1)[1])
wallet_service_instance = wallet_service_class()

register_for_existed_user_service_class_name = settings.REGISTER_FOR_EXISTED_USER_SERVICE
register_for_existed_user_service_class = getattr(importlib.import_module(register_for_existed_user_service_class_name.rsplit('.', 1)[0]), register_for_existed_user_service_class_name.rsplit('.', 1)[1])
register_for_existed_user_service_instance = register_for_existed_user_service_class()

register_for_new_user_service_class_name = settings.REGISTER_FOR_NEW_USER_SERVICE
register_for_new_user_service_class = getattr(importlib.import_module(register_for_new_user_service_class_name.rsplit('.', 1)[0]), register_for_new_user_service_class_name.rsplit('.', 1)[1])
register_for_new_user_service_instance = register_for_new_user_service_class()


cerate_order_service_class_name = settings.CREATE_ORDER_SERVICE
cerate_order_service_class = getattr(importlib.import_module(cerate_order_service_class_name.rsplit('.', 1)[0]), cerate_order_service_class_name.rsplit('.', 1)[1])
cerate_order_service_instance = cerate_order_service_class()