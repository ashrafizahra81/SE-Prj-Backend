from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=2000, null=True)
    user_postal_code = models.CharField(max_length=20, null=True)
    user_address = models.CharField(max_length=20, null=True)
    shop_name = models.CharField(max_length=1000, null=True)
    shop_address = models.CharField(max_length=20, null=True)
    shop_phone_number = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


class Category(models.Model):
    category_description = models.CharField(max_length=100, null=False)


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False)
    product_price = models.BigIntegerField(null=False)
    shop = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='products')
    upload = models.FileField(upload_to='uploads/', null=True)
    inventory = models.IntegerField(default=0, null=False)
    product_size = models.CharField(max_length=100, null=True)
    product_color = models.CharField(max_length=100, null=True)
    product_height = models.IntegerField(default=0)
    product_design = models.CharField(max_length=100, null=True)
    product_material = models.CharField(max_length=100, null=True)
    product_country = models.CharField(max_length=100, null=True)
    product_off_percent = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)
    score = models.FloatField(default=0)
    number_of_votes = models.IntegerField(default=0)
    # product_brand = models.CharField(max_length=100, null=True)
    # product_color = models.CharField(max_length=100, null=False)
    # product_size = models.CharField(max_length=100, null=False)
    # product_off_percent = models.IntegerField(null=False, default=0)
    # style_id = models.ForeignKey(Style, on_delete=models.DO_NOTHING, null = True)
    # category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null = True)
    # product_image = models.URLField(null=True)
    # file will be saved to MEDIA_ROOT / uploads / 2015 / 01 / 30


# upload = models.FileField(upload_to='uploads/% Y/% m/% d/')

class Style(models.Model):
    style_image_url = models.URLField(null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    style_param_1 = models.CharField(max_length=100, default='')
    style_param_2 = models.CharField(max_length=100, default='')
    style_param_3 = models.CharField(max_length=100, default='')
    style_param_4 = models.CharField(max_length=100, default='')
    style_param_5 = models.CharField(max_length=100, default='')


class ConstantStyles(models.Model):
    style_image_url = models.URLField(null=True)
    style_param_1 = models.CharField(max_length=100, default='')
    style_param_2 = models.CharField(max_length=100, default='')
    style_param_3 = models.CharField(max_length=100, default='')
    style_param_4 = models.CharField(max_length=100, default='')
    style_param_5 = models.CharField(max_length=100, default='')


class UserStyle(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    style_id = models.ForeignKey(Style, on_delete=models.DO_NOTHING)


class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, null=True, default="not Accepted")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, related_name='orders')
    cost = models.IntegerField()
    status = models.CharField(max_length=100, null=False)
    order_date = models.DateTimeField(auto_now_add=True, null=False)
    complete_date = models.DateTimeField(null=True)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
class UserFavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)


class ProductAndStyle(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.BigIntegerField(null=True)
    shop_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='products1')
    upload = models.FileField(upload_to='uploads/', null=True)

    product_size = models.CharField(max_length=100, null=True)
    product_height = models.IntegerField(default=0)
    product_design = models.CharField(max_length=100, null=True)
    product_material = models.CharField(max_length=100, null=True)
    product_country = models.CharField(max_length=100, null=True)
    product_off_percent = models.IntegerField(null=True, default=0)
    inventory = models.IntegerField(default=0, null=True)

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    style_param_1 = models.CharField(max_length=100, default='')
    style_param_2 = models.CharField(max_length=100, default='')
    style_param_3 = models.CharField(max_length=100, default='')
    style_param_4 = models.CharField(max_length=100, default='')
    style_param_5 = models.CharField(max_length=100, default='')


class ProductInUserFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)


class ProductInUserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
