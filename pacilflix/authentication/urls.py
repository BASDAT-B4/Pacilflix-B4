from django.urls import path
from authentication.views import show_main, register
from django.contrib.auth import authenticate, login
from authentication.views import login_user 
from django.contrib.auth import logout
from authentication.views import logout_user

app_name = 'authentication'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]