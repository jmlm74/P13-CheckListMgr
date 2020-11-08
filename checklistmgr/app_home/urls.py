"""
    home_app URL Configuration

"""
from django.urls import path

from app_home import views as ahv


app_name = 'app_home'
urlpatterns = [
    path('', ahv.Index.as_view(), name='index'),
    path('index/', ahv.Index.as_view(), name='index'),
    path('main/', ahv.MainView.as_view(), name='main'),
    path('legal/', ahv.LegalView.as_view(), name='legal'),
    path('contact/', ahv.ContactView.as_view(), name='contact'),

    # ajax autocomplete select
    path('autocomplete_search_mat/', ahv.autocomplete_search_mat, name='autosearchmat'),
    path('autocomplete_search_man/', ahv.autocomplete_search_man, name='autosearchman'),
    path('search_chklst/', ahv.search_chklst, name='searchchklst'),
]
