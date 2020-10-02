"""
    home_app URL Configuration

"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from app_user import views as auv
from app_user import company_views as aucv

app_name = 'app_user'
urlpatterns = [
    path('logout/', auv.user_logout, name='logout'),
    path('register/', auv.RegisterView.as_view(), name='register'),
    path('list/', login_required(auv.UserListView.as_view()), name='list'),
    path('edit/<int:pk>', login_required(auv.EditUserView.as_view()), name='edit'),
    path('delete_user/', login_required(auv.delete_user), name='delete'),

    path('create_company/', login_required(aucv.CreateCompanyView.as_view()), name='createcompany'),
    path('list_company/', login_required(aucv.ListCompaniesView.as_view()), name='listcompanies'),
    path('update/<int:pk>', login_required(aucv.EditCompanyView.as_view()), name='editcompany'),

    # Reset password
    path('reset_password', auv.reset_psw, name='reset_password'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="app_user/registration/reset_password_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name=
                                                      'app_user/registration/reset_password_complete.html'),
         name='password_reset_complete'),
]
