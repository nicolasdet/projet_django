"""my_project_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from user import views as user_view

urlpatterns = [
    url('admin/', admin.site.urls),
    url('register/', user_view.register, name='register'),
    url('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),
        name='password_reset'),
    url('password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    url('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url('reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    url('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url('profile/', user_view.profile, name='profile'),
    url('game/', include('game.urls'))
]
