"""
    home_app URL Configuration

"""
from django.urls import path

from app_user import views as auv


app_name = 'app_user'
urlpatterns = [
    path('logout/', auv.user_logout, name='logout'),
    path('register/', auv.RegisterView.as_view(), name='register'),
]
