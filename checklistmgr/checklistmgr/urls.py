"""checklistmgr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from app_home import views as ahv



urlpatterns = [
    path('app_home/', include('app_home.urls')),
    path('app_user/', include('app_user.urls')),
    path('app_utilities/', include('app_utilities.urls')),
    path('app_create_chklst/', include('app_create_chklst.urls')),
    path('app_input_chklst/', include('app_input_chklst.urls')),
    path('app_checklist/', include('app_checklist.urls')),
    path('', ahv.Index.as_view(), name='index'),
    path('accounts/login/', RedirectView.as_view(url='/app_home/index/')),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='app_user/registration/reset_password_complete.html'),
         name='password_reset_complete'),

]

handler400 = 'app_home.errors.handler400'
handler403 = 'app_home.errors.handler403'
handler404 = 'app_home.errors.handler404'
handler500 = 'app_home.errors.handler500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('admin/', admin.site.urls),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
