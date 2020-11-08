"""
    app_checklist URL Configuration
"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from app_checklist import saveviews as acsv
from app_checklist import views as acv
from app_checklist import pdfviews as acpv

app_name = 'app_checklist'
urlpatterns = [
    # main
    path('saisie1/<int:pk>', login_required(acv.ChekListInput1.as_view()), name='saisie1'),
    path('saisie1/', login_required(acv.ChekListInput1.as_view()), name='saisie1'),
    path('saisie2/', login_required(acv.ChekListInput2.as_view()), name='saisie2'),
    path('saisie3/', login_required(acv.ChekListInput3.as_view()), name='saisie3'),
    path('saisie4/', login_required(acsv.ChekListInput4.as_view()), name='saisie4'),
    # Check_list for private
    path('saisie3-priv/<int:pk>', login_required(acv.cheklistinput3_priv), name='saisie3-priv'),

    # Ajax
    path('getmanager/', login_required(acv.getmanager), name='getmanager'),
    path('getmaterial/', login_required(acv.getmaterial), name='getmaterial'),
    path('beforepreview/', login_required(acsv.before_preview), name='beforepreview'),

    # Photos -> Ajax
    path('upload_photos/', login_required(acsv.file_upload_view), name='upload_photos'),
    path('remove_photos/', login_required(acsv.file_remove_view), name='remove_photos'),

    # pdf
    path('pdf/', login_required(acpv.render_pdf_view), name='pdf'),
    path('pdf/<str:save>/', login_required(acpv.render_pdf_view), name='pdf'),

]
