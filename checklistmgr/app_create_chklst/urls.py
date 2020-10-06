"""
    home_app URL Configuration

"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from app_create_chklst import views as accv

app_name = 'app_create_chklst'
urlpatterns = [
    path('catlinemgmt', accv.CatandLineMgmtView, name='catlineMgmt'),
    path('catcreate/', accv.CategoryCreateView.as_view(), name='chk-catcreate'),
    path('catdisplay/<int:pk>', accv.CategoryDisplayView.as_view(), name='chk-catdisplay'),
    path('catupdate/<int:pk>', accv.CategoryUpdateView.as_view(), name='chk-catupdate'),
    path('catdelete/<int:pk>', accv.CategoryDeleteView.as_view(), name='chk-catdelete'),

    path('linecreate/', accv.LineCreateView.as_view(), name='chk-linecreate'),
    path('linedisplay/<int:pk>', accv.LineDisplayView.as_view(), name='chk-linedisplay'),
    path('lineupdate/<int:pk>', accv.LineUpdateView.as_view(), name='chk-lineupdate'),
    path('linedelete/<int:pk>', accv.LineDeleteView.as_view(), name='chk-linedelete'),

]
