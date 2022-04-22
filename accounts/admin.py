from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

UserAdmin.fieldsets += (
    ("Additional Infos", {'fields': ('user_phone_number', 'user_postal_code', 'user_address')}),
)
admin.site.register(User, UserAdmin)