from django.urls import path
from main.views import show_main
from daftar_kontributor.views import *

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
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

