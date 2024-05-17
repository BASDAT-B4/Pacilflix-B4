from django.urls import path
from trailer.views import *

app_name = 'trailer'

urlpatterns = [
    path('trailers/', get_trailers, name='trailers'),
    # path('search/', search_trailer, name='search_trailer'),  # Path untuk hasil pencarian
    path('search/', search_trailer, name='search_trailer'), 
]