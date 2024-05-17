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

def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    return wrapper

@connectdb
def show_daftar_favorit(request):
    username = "melissa31"
    daftar_favorit = get_daftar_favorit(username)

    # daftar_favorit = get_daftar_favorit()

    return render(request, "daftar_favorit.html", {'daftar_favorit': daftar_favorit})

@require_POST

def hapus_favorit(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')  # Ambil judul favorit dari POST data
        username = request.POST.get('username')  # Ambil username favorit dari POST data
        timestamp_str = request.POST.get('timestamp')
        print(judul)
       
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM pacilflix.tayangan WHERE judul = %s", [judul])
            row = cursor.fetchone()
            id_tayangan = row[0]
            print("ini id tayangan", id_tayangan)
            
        # # Hapus entri dari tabel DAFTAR_FAVORIT
        # with connection.cursor() as cursor:
        #     cursor.execute("DELETE FROM pacilflix.daftar_favorit WHERE judul = %s", [judul])

        return redirect('daftar_favorit:show_daftar_favorit')  # Redirect to the favorites list page
    else:
        return redirect('daftar_favorit:show_daftar_favorit')  # Redirect if request method is not POST
