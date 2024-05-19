from django.shortcuts import render
from django.shortcuts import render
from django.db import connection
from daftar_kontributor.query import ContributorManager
from daftar_kontributor.utils.helper import EncodeHelper
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.db.models import Count, F
from django.db import connection
from django.db.utils import OperationalError
import uuid
from typing import List, Tuple
from functools import wraps
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages


def get_user(request):
    return request.COOKIES.get('username')

# Create your views here.
def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        with connection.cursor() as cursor:
            return func(request, cursor, *args, **kwargs)
    return wrapper




@connectdb
def get_shows(request, cursor: CursorWrapper):
    # Query untuk mendapatkan tayangan film
    cursor.execute("""
        SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
        FROM pacilflix.tayangan AS t 
        JOIN pacilflix.film AS f ON t.id = f.id_tayangan
    """)
    film_list = cursor.fetchall()

    # Query untuk mendapatkan tayangan series
    cursor.execute("""
        SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
        FROM pacilflix.tayangan AS t 
        JOIN pacilflix.series AS s ON t.id = s.id_tayangan
    """)
    series_list = cursor.fetchall()

    # Tanggal sekarang
    today = datetime.date.today()
    # Tanggal 7 hari yang lalu
    seven_days_ago = today - datetime.timedelta(days=7)

    # Query untuk mendapatkan top 10 tayangan berdasarkan jumlah viewer dalam 7 hari terakhir
    cursor.execute("""
        SELECT
            ROW_NUMBER() OVER (ORDER BY SUM(view_count) DESC) AS "Peringkat",
            judul AS "Judul",
            sinopsis_trailer AS "Sinopsis Trailer",
            url_video_trailer AS "URL Trailer",
            release_date_trailer AS "Tanggal Rilis Trailer",
            SUM(view_count) AS "Total View 7 Hari Terakhir"
        FROM (
            SELECT
                T.id,
                T.judul,
                T.sinopsis_trailer,
                T.url_video_trailer,
                T.release_date_trailer,
                CASE
                    WHEN RN.end_date_time >= RN.start_date_time + (F.durasi_film * INTERVAL '1 minute' * 0.70)
                        AND RN.start_date_time BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
                        THEN 1
                    ELSE 0
                END AS view_count
            FROM pacilflix.tayangan AS T
            JOIN pacilflix.riwayat_nonton AS RN ON T.id = RN.id_tayangan
            LEFT JOIN pacilflix.film AS F ON T.id = F.id_tayangan
            UNION ALL
            SELECT
                T.id,
                T.judul,
                T.sinopsis_trailer,
                T.url_video_trailer,
                T.release_date_trailer,
                CASE
                    WHEN RN.end_date_time >= RN.start_date_time + (E.durasi * INTERVAL '1 minute' * 0.70)
                        AND RN.start_date_time BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
                        THEN 1
                    ELSE 0
                END AS view_count
            FROM pacilflix.tayangan AS T
            JOIN pacilflix.series AS S ON T.id = S.id_tayangan
            JOIN pacilflix.episode AS E ON S.id_tayangan = E.id_series
            JOIN pacilflix.riwayat_nonton AS RN ON E.id_series = RN.id_tayangan
        ) AS Combined
        GROUP BY judul, sinopsis_trailer, url_video_trailer, release_date_trailer
        ORDER BY "Total View 7 Hari Terakhir" DESC
        LIMIT 10;
    """)

    top_10_shows = cursor.fetchall()

    return render(request, 'tayangan.html', {
        'film_list': film_list,
        'series_list': series_list,
        'top_10_shows': top_10_shows
    })




@connectdb
def search_trailer(request, cursor):  # Tambahkan request di sini
    query = request.GET.get('q')
    search_results = []

    if query:
        try:
            # Lakukan pencarian tayangan berdasarkan judul menggunakan SQL
            cursor.execute("""
                SELECT judul, sinopsis_trailer, url_video_trailer, release_date_trailer
                FROM pacilflix.tayangan
                WHERE judul ILIKE %s
            """, ['%' + query + '%'])

            search_results = cursor.fetchall()
        except OperationalError as e:
            # Tangani kesalahan koneksi atau query
            print(f"Error: {e}")
            # Atau tampilkan pesan kesalahan ke pengguna

    return render(request, 'trailers.html', {'search_results': search_results})



# @connectdb
# def get_film_detail(request, cursor, film_id):
#     # if 'username' not in request.COOKIES:
#     #     return redirect(reverse('authentication:login'))

#     # Fetch film details including release_date_film and url_video_film
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.asal_negara, f.durasi_film, f.release_date_film, f.url_video_film
#         FROM pacilflix.tayangan t
#         JOIN pacilflix.film f ON t.id = f.id_tayangan
#         WHERE f.id_tayangan = %s
#     """, [film_id])
#     film = cursor.fetchone()

#     if not film:
#         return render(request, 'film_detail.html', {'error': 'Film not found'})

#     # Fetch average rating
#     cursor.execute("""
#         SELECT COALESCE(AVG(u.rating), 0)
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#     """, [film_id])
#     rating_avg = cursor.fetchone()[0]

#     # Fetch genres
#     cursor.execute("""
#         SELECT gt.genre
#         FROM pacilflix.genre_tayangan gt
#         WHERE gt.id_tayangan = %s
#     """, [film_id])
#     genres = cursor.fetchall()

#     # Fetch players
#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.memainkan_tayangan mt
#         JOIN pacilflix.contributors c ON mt.id_pemain = c.id
#         WHERE mt.id_tayangan = %s
#     """, [film_id])
#     players = cursor.fetchall()

#     # Fetch screenwriters
#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.menulis_skenario_tayangan mst
#         JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
#         WHERE mst.id_tayangan = %s
#     """, [film_id])
#     screenwriters = cursor.fetchall()

#     # Fetch director
#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.sutradara s
#         JOIN pacilflix.contributors c ON s.id = c.id
#         WHERE s.id = (
#             SELECT t.id_sutradara
#             FROM pacilflix.tayangan t
#             WHERE t.id = %s
#         )
#     """, [film_id])
#     director = cursor.fetchone()

#     # Fetch reviews
#     # cursor.execute("""
#     #     SELECT u.username, u.deskripsi, u.rating, u.timestamp
#     #     FROM pacilflix.ulasan u
#     #     WHERE u.id_tayangan = %s
#     #     ORDER BY u.timestamp DESC
#     # """, [film_id])
#     # reviews = cursor.fetchall()

#     # Fetch reviews
#     cursor.execute("""
#         SELECT u.username, u.deskripsi, u.rating, u.timestamp
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#         ORDER BY u.timestamp DESC
#     """, [film_id])
#     reviews = cursor.fetchall()

#     film_data = {
#         'judul': film[0],
#         'sinopsis': film[1],
#         'url_video_trailer': film[2],
#         'release_date_trailer': film[3],
#         'asal_negara': film[4],
#         'durasi_film': film[5],
#         'release_date_film': film[6],
#         'url_video_film': film[7],
#         'rating_avg': rating_avg,
#         'genres': [genre[0] for genre in genres],
#         'players': [player[0] for player in players],
#         'screenwriters': [screenwriter[0] for screenwriter in screenwriters],
#         'director': director[0] if director else None,
#         # 'reviews': reviews
#         'reviews': reviews

#     }

#     context = {
#         'film': film_data
#     }
#     return render(request, 'film_detail.html', context)
# # View untuk detail film
@connectdb
def get_film_detail(request, cursor, film_id):
    cursor.execute("""
        SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.asal_negara, f.durasi_film, f.release_date_film, f.url_video_film
        FROM pacilflix.tayangan t
        JOIN pacilflix.film f ON t.id = f.id_tayangan
        WHERE f.id_tayangan = %s
    """, [film_id])
    film = cursor.fetchone()

    if not film:
        return render(request, 'film_detail.html', {'error': 'Film not found'})

    cursor.execute("""
        SELECT COALESCE(AVG(u.rating), 0)
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
    """, [film_id])
    rating_avg = cursor.fetchone()[0]

    cursor.execute("""
        SELECT gt.genre
        FROM pacilflix.genre_tayangan gt
        WHERE gt.id_tayangan = %s
    """, [film_id])
    genres = cursor.fetchall()

    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.memainkan_tayangan mt
        JOIN pacilflix.contributors c ON mt.id_pemain = c.id
        WHERE mt.id_tayangan = %s
    """, [film_id])
    players = cursor.fetchall()

    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.menulis_skenario_tayangan mst
        JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
        WHERE mst.id_tayangan = %s
    """, [film_id])
    screenwriters = cursor.fetchall()

    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.sutradara s
        JOIN pacilflix.contributors c ON s.id = c.id
        WHERE s.id = (
            SELECT t.id_sutradara
            FROM pacilflix.tayangan t
            WHERE t.id = %s
        )
    """, [film_id])
    director = cursor.fetchone()

    cursor.execute("""
        SELECT u.username, u.deskripsi, u.rating, u.timestamp
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
        ORDER BY u.timestamp DESC
    """, [film_id])
    reviews = cursor.fetchall()

    # Convert release_date_film to datetime object
    # release_date_film = datetime.datetime.strptime(film[6], '%Y-%m-%d')

    film_data = {
        'judul': film[0],
        'sinopsis': film[1],
        'url_video_trailer': film[2],
        'release_date_trailer': film[3],
        'asal_negara': film[4],
        'durasi_film': film[5],
        'release_date_film': film[6],
        'url_video_film': film[7],
        'rating_avg': rating_avg,
        'genres': [genre[0] for genre in genres],
        'players': [player[0] for player in players],
        'screenwriters': [screenwriter[0] for screenwriter in screenwriters],
        'director': director[0] if director else None,
        'reviews': reviews
    }

    ratings = list(range(1, 6))  # Daftar rating dari 1 sampai 5

    context = {
        'film': film_data,
        'film_id': film_id,  # Tambahkan film_id ke context
        'ratings': ratings,  # Tambahkan daftar rating ke context
        # 'now': datetime.datetime.now()
    }
    return render(request, 'film_detail.html', context)

# View untuk detail series
# @connectdb
# def get_series_detail(request, cursor, series_id):
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.asal_negara, s.id_tayangan
#         FROM pacilflix.tayangan t
#         JOIN pacilflix.series s ON t.id = s.id_tayangan
#         WHERE s.id_tayangan = %s
#     """, [series_id])
#     series = cursor.fetchone()

#     if not series:
#         return render(request, 'series_detail.html', {'error': 'Series not found'})

#     cursor.execute("""
#         SELECT e.sub_judul, e.url_video, e.release_date
#         FROM pacilflix.episode e
#         WHERE e.id_series = %s
#     """, [series_id])
#     episodes = cursor.fetchall()

#     cursor.execute("""
#         SELECT COALESCE(AVG(u.rating), 0)
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#     """, [series_id])
#     rating_avg = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT gt.genre
#         FROM pacilflix.genre_tayangan gt
#         WHERE gt.id_tayangan = %s
#     """, [series_id])
#     genres = cursor.fetchall()

#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.memainkan_tayangan mt
#         JOIN pacilflix.contributors c ON mt.id_pemain = c.id
#         WHERE mt.id_tayangan = %s
#     """, [series_id])
#     players = cursor.fetchall()

#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.menulis_skenario_tayangan mst
#         JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
#         WHERE mst.id_tayangan = %s
#     """, [series_id])
#     screenwriters = cursor.fetchall()

#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.sutradara s
#         JOIN pacilflix.contributors c ON s.id = c.id
#         WHERE s.id = (
#             SELECT t.id_sutradara
#             FROM pacilflix.tayangan t
#             WHERE t.id = %s
#         )
#     """, [series_id])
#     director = cursor.fetchone()

#     cursor.execute("""
#         SELECT u.username, u.deskripsi, u.rating, u.timestamp
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#         ORDER BY u.timestamp DESC
#     """, [series_id])
#     reviews = cursor.fetchall()

#     series_data = {
#         'judul': series[0],
#         'sinopsis': series[1],
#         'url_video_trailer': series[2],
#         'release_date_trailer': series[3],
#         'asal_negara': series[4],
#         'episodes': [{'sub_judul': episode[0], 'url_video': episode[1], 'release_date': episode[2]} for episode in episodes],
#         'rating_avg': rating_avg,
#         'genres': [genre[0] for genre in genres],
#         'players': [player[0] for player in players],
#         'screenwriters': [screenwriter[0] for screenwriter in screenwriters],
#         'director': director[0] if director else None,
#         'reviews': reviews,
#         'id_series': series_id
#     }

#     context = {
#         'series': series_data,
#         # 'film_id': series_id,
#     }
#     return render(request, 'series_detail.html', context)

# @connectdb
# def get_series_detail(request, cursor, series_id):
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.asal_negara, s.id_tayangan
#         FROM pacilflix.tayangan t
#         JOIN pacilflix.series s ON t.id = s.id_tayangan
#         WHERE s.id_tayangan = %s
#     """, [series_id])
#     series = cursor.fetchone()

#     if not series:
#         return render(request, 'series_detail.html', {'error': 'Series not found'})

#     cursor.execute("""
#         SELECT e.sub_judul, e.url_video, e.release_date, e.id_series  
#         FROM pacilflix.episode e
#         WHERE e.id_series = %s
#     """, [series_id])
#     episodes = cursor.fetchall()

#     cursor.execute("""
#         SELECT COALESCE(AVG(u.rating), 0)
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#     """, [series_id])
#     rating_avg = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT gt.genre
#         FROM pacilflix.genre_tayangan gt
#         WHERE gt.id_tayangan = %s
#     """, [series_id])
#     genres = cursor.fetchall()

#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.memainkan_tayangan mt
#         JOIN pacilflix.contributors c ON mt.id_pemain = c.id
#         WHERE mt.id_tayangan = %s
#     """, [series_id])
#     players = cursor.fetchall()

#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.menulis_skenario_tayangan mst
#         JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
#         WHERE mst.id_tayangan = %s
#     """, [series_id])
#     screenwriters = cursor.fetchall()

#     cursor.execute("""
#         SELECT c.nama
#         FROM pacilflix.sutradara s
#         JOIN pacilflix.contributors c ON s.id = c.id
#         WHERE s.id = (
#             SELECT t.id_sutradara
#             FROM pacilflix.tayangan t
#             WHERE t.id = %s
#         )
#     """, [series_id])
#     director = cursor.fetchone()

#     cursor.execute("""
#         SELECT u.username, u.deskripsi, u.rating, u.timestamp
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#         ORDER BY u.timestamp DESC
#     """, [series_id])
#     reviews = cursor.fetchall()

#     series_data = {
#         'judul': series[0],
#         'sinopsis': series[1],
#         'url_video_trailer': series[2],
#         'release_date_trailer': series[3],
#         'asal_negara': series[4],
#         'episodes': [{'sub_judul': episode[0], 'url_video': episode[1], 'release_date': episode[2], 'id_series': episode[3]} for episode in episodes],
#         'rating_avg': rating_avg,
#         'genres': [genre[0] for genre in genres],
#         'players': [player[0] for player in players],
#         'screenwriters': [screenwriter[0] for screenwriter in screenwriters],
#         'director': director[0] if director else None,
#         'reviews': reviews
#     }

#     context = {
#         'series': series_data
#     }
#     return render(request, 'series_detail.html', context)

@connectdb
def get_series_detail(request, cursor, series_id):
    cursor.execute("""
        SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.asal_negara, s.id_tayangan
        FROM pacilflix.tayangan t
        JOIN pacilflix.series s ON t.id = s.id_tayangan
        WHERE s.id_tayangan = %s
    """, [series_id])
    series = cursor.fetchone()

    if not series:
        return render(request, 'series_detail.html', {'error': 'Series not found'})

    cursor.execute("""
        SELECT e.sub_judul, e.url_video, e.release_date, e.id_series  
        FROM pacilflix.episode e
        WHERE e.id_series = %s
    """, [series_id])
    episodes = cursor.fetchall()

    cursor.execute("""
        SELECT COALESCE(AVG(u.rating), 0)
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
    """, [series_id])
    rating_avg = cursor.fetchone()[0]

    cursor.execute("""
        SELECT gt.genre
        FROM pacilflix.genre_tayangan gt
        WHERE gt.id_tayangan = %s
    """, [series_id])
    genres = cursor.fetchall()

    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.memainkan_tayangan mt
        JOIN pacilflix.contributors c ON mt.id_pemain = c.id
        WHERE mt.id_tayangan = %s
    """, [series_id])
    players = cursor.fetchall()

    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.menulis_skenario_tayangan mst
        JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
        WHERE mst.id_tayangan = %s
    """, [series_id])
    screenwriters = cursor.fetchall()

    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.sutradara s
        JOIN pacilflix.contributors c ON s.id = c.id
        WHERE s.id = (
            SELECT t.id_sutradara
            FROM pacilflix.tayangan t
            WHERE t.id = %s
        )
    """, [series_id])
    director = cursor.fetchone()

    cursor.execute("""
        SELECT u.username, u.deskripsi, u.rating, u.timestamp
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
        ORDER BY u.timestamp DESC
    """, [series_id])
    reviews = cursor.fetchall()

    series_data = {
        'judul': series[0],
        'sinopsis': series[1],
        'url_video_trailer': series[2],
        'release_date_trailer': series[3],
        'asal_negara': series[4],
        'episodes': [{'sub_judul': episode[0], 'url_video': episode[1], 'release_date': episode[2], 'id_series': episode[3]} for episode in episodes],
        'rating_avg': rating_avg,
        'genres': [genre[0] for genre in genres],
        'players': [player[0] for player in players],
        'screenwriters': [screenwriter[0] for screenwriter in screenwriters],
        'director': director[0] if director else None,
        'reviews': reviews
    }

    ratings = list(range(1, 6))  # Daftar rating dari 1 sampai 5

    context = {
        'series': series_data,
        'series_id': series_id,  # Tambahkan series_id ke context
        'ratings': ratings,  # Tambahkan daftar rating ke context
    }

    return render(request, 'series_detail.html', context)



# View untuk menambahkan ulasan

# View untuk menambah ulasan pada seri
# def add_series_review(request, series_id):
#     if request.method == 'POST':
#         deskripsi = request.POST.get('deskripsi')
#         rating = request.POST.get('rating')

#         if not deskripsi or not rating:
#             messages.error(request, 'Deskripsi ulasan dan rating harus diisi.')
#             return redirect(reverse('tayangan:series_detail', kwargs={'series_id': series_id}))

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     INSERT INTO pacilflix_ulasan (id_tayangan, username, deskripsi, rating, timestamp)
#                     VALUES (%s, %s, %s, %s, %s)
#                 """, [series_id, 'scud', deskripsi, int(rating), datetime.now()])
#             messages.success(request, 'Ulasan berhasil ditambahkan.')
#         except Exception as e:
#             messages.error(request, f'Gagal menambahkan ulasan: {str(e)}')

#     return redirect(reverse('tayangan:series_detail', kwargs={'series_id': series_id}))




# '{request.COOKIES.get('username')}'

def add_review(request, tayangan_type, tayangan_id):
    if request.method == 'POST':
        # Periksa apakah pengguna sudah login
        # if not request.user.is_authenticated:
        #     messages.error(request, 'Anda harus login untuk menambah ulasan.')
        #     return redirect(reverse('authentication:login'))
        # username = get_user(request=request)
        # if username == None:  # kalau belum login pergi ke register
        #     return redirect('/register/')

        # Ambil deskripsi dan rating dari form
        deskripsi = request.POST.get('deskripsi')
        rating = request.POST.get('rating')

        # Periksa apakah deskripsi dan rating ada
        if not deskripsi or not rating:
            messages.error(request, 'Deskripsi ulasan dan rating harus diisi.')
            return redirect(reverse(f'tayangan:{tayangan_type}_detail', kwargs={f'{tayangan_type}_id': tayangan_id}))
        
        url = f"""INSERT INTO pacilflix.ulasan (id_tayangan, username, deskripsi, rating, timestamp)
                  VALUES ('{tayangan_id}', '{request.session.get('username')}', '{deskripsi}', '{rating}', NOW())""" 
        try:
            # Simpan ulasan ke database
            with connection.cursor() as cursor:
                cursor.execute(url)
            messages.success(request, 'Ulasan berhasil ditambahkan.')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan ulasan: {str(e)}')

        return redirect(reverse(f'tayangan:{tayangan_type}_detail', kwargs={f'{tayangan_type}_id': tayangan_id}))

    return redirect(reverse(f'tayangan:{tayangan_type}_detail', kwargs={f'{tayangan_type}_id': tayangan_id}))


    

@connectdb
def show_episode_detail(request, cursor, series_id, sub_judul):
    cursor.execute("""
        SELECT e.sub_judul, e.sinopsis, e.durasi, e.url_video, e.release_date
        FROM pacilflix.episode e
        WHERE e.id_series = %s AND e.sub_judul = %s
    """, [series_id, sub_judul])
    episode = cursor.fetchone()

    if not episode:
        return render(request, 'episode_detail.html', {'error': 'Episode not found'})

    context = {
        'episode': {
            'sub_judul': episode[0],
            'sinopsis': episode[1],
            'durasi': episode[2],
            'url_video': episode[3],
            'release_date': episode[4]
        }
    }
    return render(request, 'episode_detail.html', context)






# def add_review(request, cursor, film_id):
#     if request.method == 'POST':
#         username = get_user(request=request)
#         if username is None:
#             return redirect(reverse('authentication:login'))

#         deskripsi = request.POST.get('deskripsi')
#         rating = request.POST.get('rating')

#         if not deskripsi or not rating:
#             return redirect(request.META.get('HTTP_REFERER'))

#         try:
#             rating = int(rating)  # Konversi rating ke integer
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp
#             cursor.execute("""
#                 INSERT INTO pacilflix.ulasan (id_tayangan, username, deskripsi, rating, timestamp)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, [film_id, username, deskripsi, rating, timestamp])
#             return redirect(reverse('tayangan:film_detail', kwargs={'film_id': film_id}))
#         except Exception as e:
#             return redirect(f'{reverse("tayangan:film_detail", kwargs={"film_id": film_id})}?error={str(e)}')

#     return redirect(reverse('tayangan:film_detail', kwargs={'film_id': film_id}))

# @connectdb
# def add_review(request, cursor, film_id):
#     if request.method == 'POST':
#         username = get_user(request=request)
#         if username is None:
#             return redirect(reverse('authentication:login'))

#         deskripsi = request.POST.get('deskripsi')
#         rating = request.POST.get('rating')

#         if not deskripsi or not rating:
#             return redirect(request.META.get('HTTP_REFERER'))

#         try:
#             cursor.execute("""
#                 INSERT INTO pacilflix.ulasan (id_tayangan, username, deskripsi, rating, timestamp)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, [film_id, username, deskripsi, int(rating), datetime.now()])
#             return redirect(reverse('tayangan:film_detail', kwargs={'film_id': film_id}))
#         except Exception as e:
#             return redirect(f'{reverse("tayangan:film_detail", kwargs={"film_id": film_id})}?error={str(e)}')

#     return redirect(reverse('tayangan:film_detail', kwargs={'film_id': film_id}))