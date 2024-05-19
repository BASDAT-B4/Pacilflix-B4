# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render, redirect
# from .models import Ulasan

# def list_reviews(request, film_id):
#     # Mendapatkan ulasan untuk film dengan film_id tertentu
#     reviews = Ulasan.objects.filter(id_tayangan=film_id).order_by('-timestamp')

#     # Render template dengan ulasan yang ditemukan
#     return render(request, 'ulasan.html', {'reviews': reviews, 'film_id': film_id})

# def add_review(request, film_id):
#     if request.method == 'POST':
#         deskripsi = request.POST['deskripsi']
#         rating = request.POST['rating']
#         # Tambahkan ulasan ke database
#         Ulasan.objects.create(id_tayangan=film_id, username=request.user.username, deskripsi=deskripsi, rating=rating)
#         # Redirect kembali ke halaman ulasan setelah menambahkan ulasan baru
#         return redirect('ulasan:list_reviews', film_id=film_id)
