from django.urls import path
from daftar_favorit.views import *

app_name = 'daftar_favorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit'),
    path('show_data_favorit/', show_daftar_favorit, name='show_daftar_favorit'),
    path('hapus_favorit/', hapus_favorit, name='hapus_favorit')
    
]