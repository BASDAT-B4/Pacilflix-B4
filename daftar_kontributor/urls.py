from django.urls import path
from daftar_kontributor.views import *

app_name = 'daftar_kontributor'

urlpatterns = [
    path('contributor/', show_daftar_kontributor, name='daftar_kontributor'),
    path('contributor/<str:tipe>/', show_daftar_kontributor, name='daftar_kontributor_filtered'),
]