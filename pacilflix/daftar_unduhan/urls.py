from django.urls import path
from daftar_unduhan.views import *

app_name = 'daftar_unduhan'

urlpatterns = [
    path('', show_daftar_unduhan, name='show_daftar_unduhan'),
    path('hapus_unduhan/', hapus_unduhan, name='hapus_unduhan'),
]
