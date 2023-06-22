from Backend import settings
import importlib

userOrderService_name = settings.ORDER_SERVICE
userOrderService_class = getattr(importlib.import_module(userOrderService_name.rsplit('.', 1)[0]), userOrderService_name.rsplit('.', 1)[1])
userOrderService_instance = userOrderService_class()

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

update_product_after_deleting_service_class_name = settings.UPDATE_PRODUCT_AFTER_DELETING_SERVICE
update_product_after_deleting_service_class = getattr(importlib.import_module(update_product_after_deleting_service_class_name.rsplit('.', 1)[0]), update_product_after_deleting_service_class_name.rsplit('.', 1)[1])
update_product_after_deleting_service_instance = update_product_after_deleting_service_class()

update_product_from_editing_service_class_name = settings.UPDATE_PRODUCT_FROM_EDITING_SERVICE
update_product_from_editing_service_class = getattr(importlib.import_module(update_product_from_editing_service_class_name.rsplit('.', 1)[0]), update_product_from_editing_service_class_name.rsplit('.', 1)[1])
update_product_from_editing_service_instance = update_product_from_editing_service_class()


create_product_service_class_name = settings.CREATE_PRODUCT_SERVICE
create_product_service_class = getattr(importlib.import_module(create_product_service_class_name.rsplit('.', 1)[0]), create_product_service_class_name.rsplit('.', 1)[1])
create_product_service_instance = create_product_service_class()

filter_product_service_class_name = settings.FILTER_PRODUCT_SERVICE
filter_product_service_class = getattr(importlib.import_module(filter_product_service_class_name.rsplit('.', 1)[0]), filter_product_service_class_name.rsplit('.', 1)[1])
filter_product_service_instance = filter_product_service_class()

shopping_cart_service_class_name = settings.SHOPPING_CART_SERVICE
shopping_cart_service_class = getattr(importlib.import_module(shopping_cart_service_class_name.rsplit('.', 1)[0]), shopping_cart_service_class_name.rsplit('.', 1)[1])
shopping_cart_service_instance = shopping_cart_service_class()

get_gift_service_class_name = settings.GET_GIFT_SERVICE
get_gift_service_class = getattr(importlib.import_module(get_gift_service_class_name.rsplit('.', 1)[0]), get_gift_service_class_name.rsplit('.', 1)[1])
get_gift_service_instance = get_gift_service_class()

apply_discount_service_class_name = settings.APPLY_DISCOUNT_SERVICE
apply_discount_service_class = getattr(importlib.import_module(apply_discount_service_class_name.rsplit('.', 1)[0]), apply_discount_service_class_name.rsplit('.', 1)[1])
apply_discount_service_instance = apply_discount_service_class()

charge_wallet_service_class_name = settings.CHARGE_WALLET_SERVICE
charge_wallet_service_class = getattr(importlib.import_module(charge_wallet_service_class_name.rsplit('.', 1)[0]), charge_wallet_service_class_name.rsplit('.', 1)[1])
charge_wallet_service_instance = charge_wallet_service_class()

favorite_product_service_class_name = settings.FAVORITE_PRODUCT_SERVICE
favorite_product_service_class = getattr(importlib.import_module(favorite_product_service_class_name.rsplit('.', 1)[0]), favorite_product_service_class_name.rsplit('.', 1)[1])
favorite_product_service_instance = favorite_product_service_class()

show_favorite_products_service_class_name = settings.SHOW_FAVORITE_PRODUCTS_SERVICE
show_favorite_products_service_class = getattr(importlib.import_module(show_favorite_products_service_class_name.rsplit('.', 1)[0]), show_favorite_products_service_class_name.rsplit('.', 1)[1])
show_favorite_products_service_instance = show_favorite_products_service_class()

verify_user_to_register_service_class_name = settings.VERIFY_USER_TO_REGISTER_SERVICE
verify_user_to_register_service_class = getattr(importlib.import_module(verify_user_to_register_service_class_name.rsplit('.', 1)[0]), verify_user_to_register_service_class_name.rsplit('.', 1)[1])
verify_user_to_register_service_instance = verify_user_to_register_service_class()

show_user_info_service_class_name = settings.SHOW_USER_INFO_SERVICE
show_user_info_service_class = getattr(importlib.import_module(show_user_info_service_class_name.rsplit('.', 1)[0]), show_user_info_service_class_name.rsplit('.', 1)[1])
show_user_info_service_instance = show_user_info_service_class()

show_shop_manager_info_service_class_name = settings.SHOW_SHOP_MANAGER_INFO_SERVICE
show_shop_manager_info_service_class = getattr(importlib.import_module(show_shop_manager_info_service_class_name.rsplit('.', 1)[0]), show_shop_manager_info_service_class_name.rsplit('.', 1)[1])
show_shop_manager_info_service_instance = show_shop_manager_info_service_class()

show_products_of_shop_service_class_name = settings.SHOW_PRODUCTS_OF_SHOP_SERVICE
show_products_of_shop_service_class = getattr(importlib.import_module(show_products_of_shop_service_class_name.rsplit('.', 1)[0]), show_products_of_shop_service_class_name.rsplit('.', 1)[1])
show_products_of_shop_service_instance = show_products_of_shop_service_class()


show_order_to_shop_service_class_name = settings.SHOW_ORDER_TO_SHOP_SERVICE
show_order_to_shop_service_class = getattr(importlib.import_module(show_order_to_shop_service_class_name.rsplit('.', 1)[0]), show_order_to_shop_service_class_name.rsplit('.', 1)[1])
show_order_to_shop_service_instance = show_order_to_shop_service_class()