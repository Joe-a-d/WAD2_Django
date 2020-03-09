from django.urls import path
from . import views

app_name = "WAD2app"

urlpatterns = [
    path('' , views.home , name = 'home') ,
    path('about/' , views.about, name="about") ,
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('dogs/', views.dogs, name='dogs'),
    path('donate/', views.donate, name='donate'),

]
