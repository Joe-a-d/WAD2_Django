from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'WAD2app'

urlpatterns = [
    path('about/' , views.about, name='about') ,
    path('donate/', views.donate, name='donate'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name=''),
    path('dogs/', views.dogs, name='dogs'),
    path('newDog/', views.addDog, name='addDog'),
    path('dogs/<int:pk>/', views.dog, name='dog'),
    path('<int:pk>/favourite/', views.favourite, name='favourite'),
    path('<int:pk>/adopt/', views.adopt, name='adopt'),
    path('application/<int:pk>', views.showApplication, name='application'),
    path('forgotPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html', success_url=settings.LOGIN_URL), name='resetPassword'),
    path('profile/changePassword', auth_views.PasswordChangeView.as_view(template_name='changePassword.html', success_url='profile/',), name='changePassword'),

]
