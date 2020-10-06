"""
    home_app URL Configuration

"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from app_create_chklst import views as accv

app_name = 'app_create_chklst'
urlpatterns = [
    path('catlinemgmt/', login_required(accv.CatandLineMgmtView), name='catlineMgmt'),
    path('catcreate/', login_required(accv.CategoryCreateView.as_view()), name='chk-catcreate'),
    path('catdisplay/<int:pk>', login_required(accv.CategoryDisplayView.as_view()), name='chk-catdisplay'),
    path('catupdate/<int:pk>', login_required(accv.CategoryUpdateView.as_view()), name='chk-catupdate'),
    path('catdelete/<int:pk>', login_required(accv.CategoryDeleteView.as_view()), name='chk-catdelete'),

    path('linecreate/', login_required(accv.LineCreateView.as_view()), name='chk-linecreate'),
    path('linedisplay/<int:pk>', login_required(accv.LineDisplayView.as_view()), name='chk-linedisplay'),
    path('lineupdate/<int:pk>', login_required(accv.LineUpdateView.as_view()), name='chk-lineupdate'),
    path('linedelete/<int:pk>', login_required(accv.LineDeleteView.as_view()), name='chk-linedelete'),

]
