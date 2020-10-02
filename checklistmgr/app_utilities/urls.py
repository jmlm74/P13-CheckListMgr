"""
    home_app URL Configuration

"""
from django.urls import path

from app_utilities import views as auv


app_name = 'app_utilities'
urlpatterns = [
    path('get_message/', auv.get_message, name='get_message'),
    path('get_address/', auv.get_address, name='get_address'),
]
