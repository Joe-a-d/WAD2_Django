from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'WAD2app'

urlpatterns = [
    path('about/' , views.about, name='about') ,
    path('donate/', views.donate, name='donate'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name=''),
    path('dogs/', views.dogs, name='dogs'),
    path('newDog/', views.addDog, name='addDog'),
    path('dogs/dog/', views.dog, name='dog'),
    path('user/favourite/', views.favourite, name='favourite'),
    path('user/adopt/', views.adopt, name='adopt'),
    path('application/', views.showApplication, name='applicationTest'),
    path('application/user', views.showApplication, name='application'),
    path('application/user/accept', views.updateApplication, name='updateApplication'),
    path('application/user/approve', views.updateApplication, name='updateApplication'),
    path('forgotPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html', success_url=settings.LOGIN_URL), name='resetPassword'),
    path('profile/changePassword', auth_views.PasswordChangeView.as_view(template_name='changePassword.html', success_url='profile/',), name='changePassword'),

]
