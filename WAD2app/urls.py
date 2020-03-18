from django.urls import path
from . import views

app_name = "WAD2app"

urlpatterns = [
    path('about/' , views.about, name="about") ,
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('dogs/', views.dogs, name='dogs'),
    path('donate/', views.donate, name='donate'),
    path('forgotPassword/', auth_views.PasswordResetView.as_view(template_name='resetPassword.html', success_url=LOGIN_URL)),
    path('profile/changePassword', auth_views.PasswordChangeView.as_view(template_name='changePassword.html', success_url='profile/',post_reset_login=True,)),
    #staff -> dashboard

]
