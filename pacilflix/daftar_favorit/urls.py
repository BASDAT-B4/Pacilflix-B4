from django.urls import path
from daftar_favorit.views import show_main, create_product
from django.contrib import admin

app_name = 'daftar_favorit'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product', create_product, name='create_product'),
]