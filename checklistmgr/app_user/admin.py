from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser

from app_user.models import User, UserLanguages, Company

# admin.site.register(User, UserAdmin)
admin.site.register(User)
admin.site.register(UserLanguages)
admin.site.register(Company)
