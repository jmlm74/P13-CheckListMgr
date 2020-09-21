"""
    home_app URL Configuration

"""
from django.urls import path

from app_home import views as ahv


app_name = 'app_home'
urlpatterns = [
    path('', ahv.Index.as_view(), name='index'),
    path('index/', ahv.Index.as_view(), name='index'),
    path('legal/', ahv.LegalView.as_view(), name='legal'),
    path('contact/', ahv.ContactView.as_view(), name='contact'),
]
