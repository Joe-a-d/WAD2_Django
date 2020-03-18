from django.urls import path
from . import views

app_name = 'WAD2app'

urlpatterns = [
    path('about/' , views.about, name='about') ,
    path('contact', views.contact, name='contact'),
    path('help%20us', views.donate, name='donate'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name=''),
    path('dogs/', views.dogs, name='dogs'),
    path('dogs/<int:dog_id>', view.dog, name='dog'),
    path('<int:dog_id>/favourite/', views.favourite, name='favourite'),
    path('<int:dog_id>/adopt/', views.adopt, name='adopt'),
    path('forgotPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html', success_url=LOGIN_URL), name='resetPassword'),
    path('profile/changePassword', auth_views.PasswordChangeView.as_view(template_name='changePassword.html', success_url='profile/',post_reset_login=True,), name='changePassword'),

]
