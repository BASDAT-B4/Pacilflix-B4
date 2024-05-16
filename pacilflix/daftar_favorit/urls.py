from django.urls import path
from daftar_favorit.views import show_main

app_name = 'daftar_favorit'

urlpatterns = [
    path('', show_main, name='show_daftar_favorit'),
]