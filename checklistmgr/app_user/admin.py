from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app_user.models import User, UserLanguages, Company

admin.site.register(User, UserAdmin)
admin.site.register(UserLanguages)
admin.site.register(Company)
