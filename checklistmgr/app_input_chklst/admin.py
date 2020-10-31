from django.contrib import admin

# Register your models here.
from app_input_chklst.models import Manager, Material
admin.site.register(Manager)
admin.site.register(Material)
