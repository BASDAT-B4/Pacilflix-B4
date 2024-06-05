from django.shortcuts import render
from functools import wraps
from daftar_unduhan.query import get_daftar_unduhan

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    return wrapper

def get_user(request):
    return request.session.get('username')

@connectdb

def show_daftar_unduhan(request):
    username = get_user(request)
    if username is None:
        return render(request, "error.html", {'message': 'User not logged in'})
    
    daftar_unduhan = get_daftar_unduhan(username)
    return render(request, "daftar_unduhan.html", {'daftar_unduhan': daftar_unduhan})


from django.shortcuts import render, redirect
from django.db import connection

from django.shortcuts import redirect

#-------- tanpa trigger ----------------

# def hapus_unduhan(request):
#     if request.method == 'POST':
#         judul = request.POST.get('judul')
#         timestamp = request.POST.get('timestamp')
#         username = request.POST.get('username')
#         id_tayangan = request.POST.get('id_tayangan')

#         with connection.cursor() as cursor:
#             # Hapus entri dari tabel TAYANGAN_TERUNDUH
#             cursor.execute("DELETE FROM pacilflix.tayangan_terunduh WHERE username = %s AND id_tayangan = %s", [username, id_tayangan])

#         # Redirect kembali ke halaman show_daftar_unduhan setelah penghapusan berhasil
#         return redirect('daftar_unduhan:show_daftar_unduhan')
#     else:
#         # Jika bukan metode POST, juga redirect ke halaman show_daftar_unduhan
#         return redirect('daftar_unduhan:show_daftar_unduhan')

#-------- dengan trigger ----------------
    
from django.shortcuts import render, redirect
from django.db import connection

def hapus_unduhan(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        timestamp = request.POST.get('timestamp')
        username = request.POST.get('username')
        id_tayangan = request.POST.get('id_tayangan')

        # Tambahkan kondisi untuk menampilkan pesan kesalahan jika penghapusan tidak dapat dilakukan
        try:
            with connection.cursor() as cursor:
                # Hapus entri dari tabel TAYANGAN_TERUNDUH
                cursor.execute("DELETE FROM pacilflix.tayangan_terunduh WHERE username = %s AND id_tayangan = %s", [username, id_tayangan])
        except Exception as e:
            error_message = str(e)
            return render(request, "daftar_unduhan.html", {'error_message': error_message})

        # Redirect kembali ke halaman show_daftar_unduhan setelah penghapusan berhasil
        return redirect('daftar_unduhan:show_daftar_unduhan')
    else:
        # Jika bukan metode POST, juga render halaman show_daftar_unduhan
        return render(request, "daftar_unduhan.html")
