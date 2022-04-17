from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, USER_NAME, password=None):
        if not email:
            raise TypeError("Users must have an email address")
        if not USER_NAME:
            raise TypeError("Users must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username = USER_NAME,
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    def create_sueruser(self, email, USER_NAME, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=USER_NAME,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user



class User(AbstractBaseUser):

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    USER_PASSWORD = models.CharField(max_length=100)
    USER_NAME = models.CharField(max_length=1000, unique=True)
    USER_PHONE_NUM = models.IntegerField()
    USER_POSTAL_CODE = models.IntegerField()
    USER_ADDRESS = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['USER_NAME']

    objects = MyAccountManager

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


    
