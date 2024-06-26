from django.shortcuts import render
from functools import wraps
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import DaftarFavorit  # Import your model

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import DaftarFavorit  # Import your model
from datetime import datetime

# Import the function from database.py
from daftar_favorit.query import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps

def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    return wrapper

def get_user(request):
    return request.session.get('username')

@connectdb

def show_daftar_favorit(request):
    username = get_user(request)
    if username is None:
        return render(request, "error.html", {'message': 'User not logged in'})

    daftar_favorit = get_daftar_favorit(username)
    return render(request, "daftar_favorit.html", {'daftar_favorit': daftar_favorit})
@require_POST

def hapus_favorit(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')  # Ambil judul favorit dari POST data
        username = request.POST.get('username')  # Ambil username favorit dari POST data
        timestamp_str = request.POST.get('timestamp')
        print(timestamp_str) 
    
        
        # Hapus entri dari tabel TAYANGAN_MEMILIKI_DAFTAR_FAVORIT yang sesuai dengan judul dan username yang dihapus sebelumnya di tabel DAFTAR_FAVORIT
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM pacilflix.tayangan_memiliki_daftar_favorit WHERE timestamp = %s AND username = %s", [timestamp_str, username])

        # Hapus entri dari tabel DAFTAR_FAVORIT
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM pacilflix.daftar_favorit WHERE judul = %s", [judul])

        return redirect('daftar_favorit:show_daftar_favorit')  # Redirect to the favorites list page
    else:
        return redirect('daftar_favorit:show_daftar_favorit')  # Redirect if request method is not POST
