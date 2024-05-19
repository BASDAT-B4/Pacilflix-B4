from django.urls import path
from tayangan.views import *
# from .views import check_trailer, show_daftar_kontributor, random

app_name = 'tayangan'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('search/', search_trailer, name='search_trailer'),  
    path('shows/', get_shows, name='shows'),
    # path('tayangan/', get_shows, name='tayangan'),
    # path('film/<uuid:film_id>/', get_film_detail, name='film_detail'), 
    path('film/<uuid:film_id>/', get_film_detail, name='film_detail'),
    # path('film/<uuid:film_id>/', film_reviews, name='film_detail'),
    # path('film/<uuid:film_id>/reviews/', film_reviews, name='film_reviews'),
    # path('film/<uuid:film_id>/add_review/', add_review, name='add_review'),
    # path('film/<uuid:film_id>/reviews/', film_reviews, name='film_reviews'),
    # path('film/<uuid:film_id>/reviews/', film_reviews, name='film_reviews'), 
    path('series/<uuid:series_id>/', get_series_detail, name='series_detail'),
    # path('film/<uuid:film_id>/add_review/', add_review, name='add_review'),
    path('film/<uuid:film_id>/', get_film_detail, name='film_detail'),
    # path('film/<uuid:film_id>/add_review/', add_review, name='add_review'),
    # path('series/<uuid:series_id>/add_review/', add_review, name='add_review'),
    # Tambahkan path untuk menambah ulasan pada seri
    # path('series/<uuid:series_id>/add_review/', add_series_review, name='add_series_review'),
    path('series/<uuid:series_id>/episode/<str:sub_judul>/', show_episode_detail, name='episode_detail'),
    # path('tayangan/<str:id_tayangan>/episode/<str:sub_judul>/',show_episode, name='episode'),
    path('<str:tayangan_type>/<uuid:tayangan_id>/add_review/', add_review, name='add_review'),
    # path('<str:tayangan_type>/<uuid:tayangan_id>/add_review/', add_review, name='add_review'),
# 

]
