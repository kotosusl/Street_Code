from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/player/', views.register_player, name='register_player'),
    path('register/organizer/', views.register_organizer, name='register_organizer'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.profile, name='profile'),
]