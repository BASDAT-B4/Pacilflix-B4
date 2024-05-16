from django.urls import path
from trailer.views import trailer_home

app_name = 'trailer'

urlpatterns = [
    path('trailer_home/', trailer_home, name='trailer_home'),  
]