from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

UserAdmin.fieldsets += (
    ("Additional Infos", {'fields': ['user_phone_number']}),
)
admin.site.register(User, UserAdmin)