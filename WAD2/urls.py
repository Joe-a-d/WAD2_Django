"""WAD2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from WAD2app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("WAD2app.urls")),
    path('forgotPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html', success_url=LOGIN_URL)),
    path('profile/changePassword', auth_views.PasswordChangeView.as_view(template_name='changePassword.html', success_url='profile/',post_reset_login=True,)),
]
