"""
    home_app URL Configuration

"""
from django.urls import path

from app_checklist import views as acv

app_name = 'app_checklist'
urlpatterns = [
    path('saisie1/<int:pk>', acv.ChekListInput1.as_view(), name='saisie1'),
    path('saisie1/', acv.ChekListInput1.as_view(), name='saisie1'),
    path('saisie2/', acv.ChekListInput2.as_view(), name='saisie2'),
    path('saisie3/', acv.ChekListInput3.as_view(), name='saisie3'),

    # Ajax
    path('getmanager/', acv.getmanager, name='getmanager'),
    path('getmaterial/', acv.getmaterial, name='getmaterial'),


]
