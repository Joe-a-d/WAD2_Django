from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'WAD2app'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/' , views.about, name='about'),
    path('contact/' , views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register_profile/<id>', views.registerProfile, name="registerProfile"),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name=''),
    path('dogs/', views.dogs, name='dogs'),
    path('newDog/', views.addDog, name='addDog'),
    path('dogs/<int:pk>/', views.dog, name='dog'),
    path('<int:pk>/favourite/', views.favourite, name='favourite'),
    path('<int:pk>/adopt/', views.adopt, name='adopt'),
    path('application/', views.showApplication, name='applicationTest'),
    path('application/<int:pk>', views.showApplication, name='application'),
    path('application/<int:pk>/accept', views.updateApplication, name='updateApplication'),
    path('application/<int:pk>/approve', views.updateApplication, name='updateApplication'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='changePassword.html'), name='changePassword'),

]
