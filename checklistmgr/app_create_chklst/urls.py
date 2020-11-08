from django.contrib.auth.decorators import login_required
from django.urls import path

from app_create_chklst import views as accv
from app_create_chklst import chklst_views as accclv

app_name = 'app_create_chklst'
urlpatterns = [
    # Main page for Cheklists
    path('mainchklst/', login_required(accclv.MainChkLstView.as_view()), name='chk-main'),

    # categories and lines tables
    path('catlinemgmt/', login_required(accv.CatandLineMgmtView), name='catlineMgmt'),

    # categories
    path('catcreate/', login_required(accv.CategoryCreateView.as_view()), name='chk-catcreate'),
    path('catdisplay/<int:pk>', login_required(accv.CategoryDisplayView.as_view()), name='chk-catdisplay'),
    path('catupdate/<int:pk>', login_required(accv.CategoryUpdateView.as_view()), name='chk-catupdate'),
    path('catdelete/<int:pk>', login_required(accv.CategoryDeleteView.as_view()), name='chk-catdelete'),
    path('catmgmt/', login_required(accv.CategoryMgmtView.as_view()), name='chk-catmgmt'),

    # lines
    path('linecreate/', login_required(accv.LineCreateView.as_view()), name='chk-linecreate'),
    path('linedisplay/<int:pk>', login_required(accv.LineDisplayView.as_view()), name='chk-linedisplay'),
    path('lineupdate/<int:pk>', login_required(accv.LineUpdateView.as_view()), name='chk-lineupdate'),
    path('linedelete/<int:pk>', login_required(accv.LineDeleteView.as_view()), name='chk-linedelete'),
    path('linemgmt/', login_required(accv.LineMgmtView.as_view()), name='chk-linemgmt'),

    # ckeck-lists
    path('chkcreate/', login_required(accclv.ChkLstCreateView.as_view()), name='chk-chklstcreate'),
    path('chklstdelete/<int:pk>', login_required(accclv.ChklstDeleteView.as_view()), name='chk-chkdelete'),
    path('chklstdisplay/<int:pk>', login_required(accclv.ChklstDisplayView.as_view()), name='chk-chkdisplay'),
    path('chklstupdate/<int:pk>', login_required(accclv.ChkLstUpdateView.as_view()), name='chk-chkupdate'),

    # Ajax create chklst
    path('create_chklst/', login_required(accclv.create_chklst), name='create_chklst'),
]
