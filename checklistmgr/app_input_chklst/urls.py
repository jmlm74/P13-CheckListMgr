from django.contrib.auth.decorators import login_required
from django.urls import path

from app_input_chklst import views as aicv
from app_input_chklst import managerviews as aicmgrv
from app_input_chklst import addressviews as aicaddrv
from app_input_chklst import materialviews as aicmatv


app_name = 'app_input_chklst'
urlpatterns = [
    # Main page for input Cheklists
    path('maininput/', login_required(aicv.MainInputView.as_view()), name='inp-main'),

    # Managers
    path('managermgmt/', login_required(aicmgrv.MgrMgmtView.as_view()), name='inp-mgrmgmt'),
    path('managercreate/<slug:return_url>', login_required(aicmgrv.ManagerCreateView.as_view()), name='inp-mgrcreate'),
    path('managercreate/', login_required(aicmgrv.ManagerCreateView.as_view()), name='inp-mgrcreate'),
    path('managerdisplay/<int:pk>', login_required(aicmgrv.ManagerDisplayView.as_view()), name='inp-mgrdisplay'),
    path('managerupdate/<int:pk>', login_required(aicmgrv.ManagerUpdateView.as_view()), name='inp-mgrupdate'),
    path('managerdelete/<int:pk>', login_required(aicmgrv.ManagerDeleteView.as_view()), name='inp-mgrdelete'),

# Adresses
    path('addressmgmt/', login_required(aicaddrv.AddressMgmtView.as_view()), name='inp-addrmgmt'),
    path('addresscreate/', login_required(aicaddrv.AddressCreateView.as_view()), name='inp-addrcreate'),
    path('addressdisplay/<int:pk>', login_required(aicaddrv.AddressDisplayView.as_view()), name='inp-addrdisplay'),
    path('addressupdate/<int:pk>', login_required(aicaddrv.AddressUpdateView.as_view()), name='inp-addrupdate'),
    path('addressdelete/<int:pk>', login_required(aicaddrv.AddressDeleteView.as_view()), name='inp-addrdelete'),

# Materials
    path('materialcreate/', login_required(aicmatv.MaterialCreateView.as_view()), name='inp-matcreate'),
    path('materialcreate/<slug:return_url>', login_required(aicmatv.MaterialCreateView.as_view()), name='inp-matcreate'),
    path('materialdisplay/<int:pk>', login_required(aicmatv.MaterialDisplayView.as_view()), name='inp-matdisplay'),
    path('materialupdate/<int:pk>', login_required(aicmatv.MaterialUpdateView.as_view()), name='inp-matupdate'),
    path('materialdelete/<int:pk>', login_required(aicmatv.MaterialDeleteView.as_view()), name='inp-matdelete'),
]
