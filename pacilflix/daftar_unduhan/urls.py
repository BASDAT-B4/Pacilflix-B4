from django.urls import path
from daftar_unduhan.views import show_main

app_name = 'daftar_unduhan'

urlpatterns = [
    path('', show_main, name='show_daftar_unduhan'),
]