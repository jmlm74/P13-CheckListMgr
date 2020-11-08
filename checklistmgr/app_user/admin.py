from django.contrib import admin

from app_user.models import User, UserLanguages, Company, Address

admin.site.register(User)
admin.site.register(UserLanguages)
admin.site.register(Company)
admin.site.register(Address)