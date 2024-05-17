from django.urls import path
from daftar_kontributor.views import *
# from .views import check_trailer, show_daftar_kontributor, random

app_name = 'daftar_kontributor'

urlpatterns = [
    path('contributor/', show_daftar_kontributor, name='daftar_kontributor'),
    path('contributor/<str:type>/', show_daftar_kontributor, name='daftar_kontributor_filtered'),
    path('random/', random, name='random'),
    # path('check_trailer/', check_trailer, name='check_trailer'),
    path('trailers/', get_trailers, name='trailers'),
    # path('search/', search_trailer, name='search_trailer'),  # Path untuk hasil pencarian
    path('search/', search_trailer, name='search_trailer'),  
    path('shows/', get_shows, name='shows'),
    # path('film/<uuid:film_id>/', get_film_detail, name='film_detail'), 
    path('film/<uuid:film_id>/', get_film_detail, name='film_detail'),
    # path('film/<uuid:film_id>/', film_reviews, name='film_detail'),
    # path('film/<uuid:film_id>/reviews/', film_reviews, name='film_reviews'),
    path('film/<uuid:film_id>/add_review/', add_review, name='add_review'),
    path('film/<uuid:film_id>/reviews/', film_reviews, name='film_reviews'),
    # path('film/<uuid:film_id>/reviews/', film_reviews, name='film_reviews'), 
    path('series/<uuid:series_id>/', get_series_detail, name='series_detail'),
]