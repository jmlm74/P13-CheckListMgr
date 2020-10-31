from django.contrib import admin
from app_create_chklst.models import Line,CheckList,Category,CheckListCategory,CheckListLine
# Register your models here.
admin.site.register(Line)
admin.site.register(CheckList)
admin.site.register(CheckListCategory)
admin.site.register(CheckListLine)
admin.site.register(Category)
