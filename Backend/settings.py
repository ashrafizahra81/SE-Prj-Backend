"""
Django settings for Backend project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^)d9q^#ccxq0uu&o+2a-n&z-g+l75cv=^jqxw2$#hcodezv(kd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = False
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'favoriteProducts.apps.FavoriteproductsConfig',
    'gifts.apps.GiftsConfig',
    'orders.apps.OrdersConfig',
    'products.apps.ProductsConfig',
    'shoppingCarts.apps.ShoppingcartsConfig',
    'wallets.apps.WalletsConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    # 'django_dump_load_utf8',
    # 'rest_framework_swagger',
    # 'drf_yasg',
    # "rest_framework_tracking",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'Backend.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1)
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply.sabkino@gmail.com'
EMAIL_HOST_PASSWORD = 'Salam@123456'
EMAIL_PORT = 587

import logging.config
import logging.handlers
import logging

FORMATTERS = (
    {
        "verbose": {
            "format": "{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}",
            "style": "{",
        },
    },
)


HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "level": "INFO"
    },
    "info_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "./logs/INFO.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "verbose",
        "level": "INFO",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    "error_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "./logs/ERROR.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "verbose",
        "level": "WARNING",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
}

LOGGERS = (
    {
        "django": {
            "handlers": ["console_handler", "info_handler"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["error_handler"],
            "level": "INFO",
            "propagate": True,
        }
    },
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}

ORDER_SERVICE = 'orders.services.order_service.UserOrderService'
PURCHASE_SERVICE = 'orders.services.order_service.Purchase'
MAIL_SERVICE = 'accounts.services.mail_service.ConcreteMailService'
UNIQUECODE_SERVICE = 'accounts.services.uniqueCode_service.ConcreteUniqueCodeService'
CODEFORUSERS_SERVICE = 'accounts.services.codeForUsers_service.ConcreteCodeForUsersService'
USER_SERVICE = 'accounts.services.user_service.ConcreteUserService'
WALLET_SERVICE = 'wallets.services.wallet_service.ConcreteWalletService'
REGISTER_FOR_EXISTED_USER_SERVICE = 'accounts.services.register_service.ConcreteUserRegisterServiceForExistedUser'
REGISTER_FOR_NEW_USER_SERVICE = 'accounts.services.register_service.ConcreteUserRegisterServiceForNewUser'
CREATE_ORDER_SERVICE = 'orders.services.order_service.ConcreteCreateOrder'

UPDATE_PRODUCT_AFTER_DELETING_SERVICE = 'products.services.product_services.ConcreteUpdateProductForDeletedProduct'
UPDATE_PRODUCT_FROM_EDITING_SERVICE = 'products.services.product_services.ConcreteUpdateProductByEditing'
CREATE_PRODUCT_SERVICE = 'products.services.product_services.ConcreteCreateProduct' 
FILTER_PRODUCT_SERVICE = 'products.services.product_services.ConcreteFilterProduct' 
SHOPPING_CART_SERVICE = 'shoppingCarts.services.shopping_cart_service.ConcreteShoppingCart' 

GET_GIFT_SERVICE = 'gifts.services.get_gift_service.ConcreteGetGiftService'
APPLY_DISCOUNT_SERVICE = 'gifts.services.apply_discount_service.ConcreteApplyDiscountService'
CHARGE_WALLET_SERVICE = 'wallets.services.charge_wallet_service.ConcreteChargeWalletService'
FAVORITE_PRODUCT_SERVICE = 'favoriteProducts.services.favorite_product_service.ConcreteFavoriteProductService'
SHOW_FAVORITE_PRODUCTS_SERVICE = 'favoriteProducts.services.show_favorite_products_service.ConcreteShowFavoriteProductService'
VERIFY_USER_TO_REGISTER_SERVICE = 'accounts.services.verify_user_to_register_service.ConcreteVerfyUserToResgisterService'
SHOW_USER_INFO_SERVICE = 'accounts.services.show_user_info_service.ConcreteShowUserInfoService'
SHOW_SHOP_MANAGER_INFO_SERVICE = 'accounts.services.show_user_info_service.ConcreteShowShopManagerInfoService'

