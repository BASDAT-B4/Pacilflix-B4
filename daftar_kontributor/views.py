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

# Create your views here.
# def connectdb(func):
#     def wrapper(request):
#         with connection.cursor() as cursor:
#             return func(cursor, request)
#     return wrapper

# @connectdb
# def random(cursor: CursorWrapper, request):
#     cursor.execute("SELECT * FROM pengguna")
#     pengguna = cursor.fetchall()
#     print(pengguna)
#     return HttpResponse(status = 200)

# def query_add(query):
#   connection.cursor().execute(query)
#   connection.close()

# def query_result(query):
#   with connection.cursor() as cursor:
#     cursor.execute(query)
#     result = cursor.fetchall()
#     return result

# def parse(result):
#     data = result[0][0]
#     return data

# def cek_koneksi_db(request):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM TAYANGAN")
#             rows = cursor.fetchall()
#             columns = [col[0] for col in cursor.description]
        
#         # Buat HTML untuk menampilkan hasil query
#         html = "<h1>Daftar Kontributor</h1>"
#         html += "<table border='1'><tr>"
        
#         # Tambahkan header tabel
#         for column in columns:
#             html += f"<th>{column}</th>"
#         html += "</tr>"
        
#         # Tambahkan baris data
#         for row in rows:
#             html += "<tr>"
#             for cell in row:
#                 html += f"<td>{cell}</td>"
#             html += "</tr>"
#         html += "</table>"
        
#         return HttpResponse(html)
#     except Exception as e:
#         return HttpResponse(f"Error: {e}")

# from django.db import connection

# def query_add(query):
#   connection.cursor().execute(query)
#   connection.close()

# def query_result(query):
#   with connection.cursor() as cursor:
#     cursor.execute(query)
#     result = cursor.fetchall()
#     return result

# def parse(result):
#     data = result[0][0]
#     return data

# print(query_result("SELECT * FROM TAYANGAN"))

# Create your views here.
# def connectdb(func):
#     def wrapper(request):
#         with connection.cursor() as cursor:
#             return func(cursor, request)
#     return wrapper
def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        with connection.cursor() as cursor:
            return func(request, cursor, *args, **kwargs)
    return wrapper

# def connectdb(func):
#     def wrapper(request):
#         with connection.cursor() as cursor:
#             return func(cursor, request)
#     return wrapper


@connectdb
def random(cursor: CursorWrapper, request):
    cursor.execute("SELECT * FROM pacilflix.pengguna")
    pengguna = cursor.fetchall()
    print(pengguna)
    return HttpResponse(status = 200)

@connectdb
def show_daftar_kontributor(request, type='all'):
    cursor = connection.cursor()
    
    if type.lower() == 'all':
        cursor.execute(ContributorManager.get_all_contributors())
    elif type.lower() == 'sutradara':
        cursor.execute(ContributorManager.filter_by_sutradara())
    elif type.lower() == 'pemain':
        cursor.execute(ContributorManager.filter_by_pemain())
    elif type.lower() == 'penulis skenario':
        cursor.execute(ContributorManager.filter_by_penulis_skenario())
    
    contributors = EncodeHelper.toSQL(cursor)

    for contributor in contributors:
        contributor['jenis_kelamin'] = 'Laki-laki' if contributor['jenis_kelamin'] == '0' else 'Perempuan'

    return render(request, "list_contributor.html", {'contributors': contributors, 'param': type})

# @connectdb
# def check_trailer(cursor: CursorWrapper, request):
#     try:
#         cursor.execute("SELECT * FROM pacilflix.trailer")
#         trailers = cursor.fetchall()
#         if trailers:
#             response = "<h1>Daftar Trailer</h1>"
#             response += "<table border='1'><tr>"
#             columns = [col[0] for col in cursor.description]
#             for column in columns:
#                 response += f"<th>{column}</th>"
#             response += "</tr>"
            
#             for row in trailers:
#                 response += "<tr>"
#                 for cell in row:
#                     response += f"<td>{cell}</td>"
#                 response += "</tr>"
#             response += "</table>"
#         else:
#             response = "<h1>Tidak ada data trailer yang tersedia</h1>"
#         return HttpResponse(response)
#     except Exception as e:
#         return HttpResponse(f"Error: {e}")
    
# def get_trailers(request):
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM tayangan")
#     tayangan_list = cursor.fetchall()

#     connection.close()

#     return render(request, 'daftar_kontributor/trailers.html', {'tayangan_list': tayangan_list})

# @connectdb
# def get_trailers(cursor: CursorWrapper, request):
#     cursor.execute("SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM pacilflix.tayangan")
#     tayangan_list = cursor.fetchall()
    
#     trailers_html = "<h1>Daftar Trailer Tayangan</h1>"
#     trailers_html += "<table border='1'><tr><th>Judul</th><th>Sinopsis</th><th>Trailer</th><th>Tanggal Rilis</th></tr>"
    
#     for tayangan in tayangan_list:
#         trailers_html += f"<tr><td>{tayangan[0]}</td><td>{tayangan[1]}</td><td><a href='{tayangan[2]}'>Tonton Trailer</a></td><td>{tayangan[3]}</td></tr>"

#     trailers_html += "</table>"

#     return HttpResponse(trailers_html)

# @connectdb
# def get_trailers(cursor: CursorWrapper, request):
#     # Query untuk mendapatkan trailer film
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer 
#         FROM pacilflix.tayangan AS t 
#         JOIN pacilflix.film AS f ON t.id = f.id_tayangan
#     """)
#     film_list = cursor.fetchall()

#     # Query untuk mendapatkan trailer series
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer 
#         FROM pacilflix.tayangan AS t 
#         JOIN pacilflix.series AS s ON t.id = s.id_tayangan
#     """)
#     series_list = cursor.fetchall()
    
#     # Menggabungkan trailer film dan series dalam satu variabel
#     trailers_html = "<h1>Daftar Trailer Film</h1>"
#     trailers_html += "<table border='1'><tr><th>Judul</th><th>Sinopsis</th><th>Trailer</th><th>Tanggal Rilis</th></tr>"
#     for film in film_list:
#         trailers_html += f"<tr><td>{film[0]}</td><td>{film[1]}</td><td><a href='{film[2]}'>Tonton Trailer</a></td><td>{film[3]}</td></tr>"
#     trailers_html += "</table>"
    
#     trailers_html += "<h1>Daftar Trailer Series</h1>"
#     trailers_html += "<table border='1'><tr><th>Judul</th><th>Sinopsis</th><th>Trailer</th><th>Tanggal Rilis</th></tr>"
#     for series in series_list:
#         trailers_html += f"<tr><td>{series[0]}</td><td>{series[1]}</td><td><a href='{series[2]}'>Tonton Trailer</a></td><td>{series[3]}</td></tr>"
#     trailers_html += "</table>"
    
#     return HttpResponse(trailers_html)

# @connectdb
# def get_top_10_trailers(cursor: CursorWrapper, request):
#     # Tanggal sekarang
#     today = datetime.date.today()
#     # Tanggal 7 hari yang lalu
#     seven_days_ago = today - datetime.timedelta(days=7)

#     # Query untuk mendapatkan top 10 tayangan berdasarkan jumlah viewer dalam 7 hari terakhir
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, COUNT(*) as total_views
#         FROM pacilflix.tayangan AS t
#         JOIN pacilflix.riwayat_nonton AS r ON t.id = r.id_tayangan
#         WHERE r.watch_time >= 0.7 * t.durasi AND r.date_watched BETWEEN %s AND %s
#         GROUP BY t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer
#         ORDER BY total_views DESC
#         LIMIT 10
#     """, [seven_days_ago, today])
#     top_10_trailers = cursor.fetchall()

#     return render(request, 'top_10_trailers.html', {'top_10_trailers': top_10_trailers})

@connectdb
def get_trailers(request, cursor):
    # Query untuk mendapatkan trailer film
    cursor.execute("""
        SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
        FROM pacilflix.tayangan AS t 
        JOIN pacilflix.film AS f ON t.id = f.id_tayangan
    """)
    film_list = cursor.fetchall()

    # Query untuk mendapatkan trailer series
    cursor.execute("""
        SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer 
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

    top_10_trailers = cursor.fetchall()

    return render(request, 'trailers.html', {
        'film_list': film_list,
        'series_list': series_list,
        'top_10_trailers': top_10_trailers
    })

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

    return render(request, 'shows.html', {
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
#     # Query untuk mendapatkan detail film berdasarkan film_id
#     cursor.execute("""
#         SELECT 
#             t.judul, 
#             t.sinopsis, 
#             f.url_video_film, 
#             f.release_date_film, 
#             f.durasi_film
#         FROM 
#             pacilflix.tayangan AS t 
#         JOIN 
#             pacilflix.film AS f ON t.id = f.id_tayangan
#         WHERE 
#             f.id_tayangan = %s
#     """, [film_id])
#     film_detail = cursor.fetchone()

#     if film_detail:
#         return render(request, 'film_detail.html', {'film': film_detail})
#     else:
#         return HttpResponse("Film not found", status=404)

@connectdb
def get_film_detail(request, cursor, film_id):
    # if 'username' not in request.COOKIES:
    #     return redirect(reverse('authentication:login'))

    # Fetch film details including release_date_film and url_video_film
    cursor.execute("""
        SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.asal_negara, f.durasi_film, f.release_date_film, f.url_video_film
        FROM pacilflix.tayangan t
        JOIN pacilflix.film f ON t.id = f.id_tayangan
        WHERE f.id_tayangan = %s
    """, [film_id])
    film = cursor.fetchone()

    if not film:
        return render(request, 'film_detail.html', {'error': 'Film not found'})

    # Fetch average rating
    cursor.execute("""
        SELECT COALESCE(AVG(u.rating), 0)
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
    """, [film_id])
    rating_avg = cursor.fetchone()[0]

    # Fetch genres
    cursor.execute("""
        SELECT gt.genre
        FROM pacilflix.genre_tayangan gt
        WHERE gt.id_tayangan = %s
    """, [film_id])
    genres = cursor.fetchall()

    # Fetch players
    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.memainkan_tayangan mt
        JOIN pacilflix.contributors c ON mt.id_pemain = c.id
        WHERE mt.id_tayangan = %s
    """, [film_id])
    players = cursor.fetchall()

    # Fetch screenwriters
    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.menulis_skenario_tayangan mst
        JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
        WHERE mst.id_tayangan = %s
    """, [film_id])
    screenwriters = cursor.fetchall()

    # Fetch director
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

    # Fetch reviews
    # cursor.execute("""
    #     SELECT u.username, u.deskripsi, u.rating, u.timestamp
    #     FROM pacilflix.ulasan u
    #     WHERE u.id_tayangan = %s
    #     ORDER BY u.timestamp DESC
    # """, [film_id])
    # reviews = cursor.fetchall()

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
        # 'reviews': reviews
    }

    context = {
        'film': film_data
    }
    return render(request, 'film_detail.html', context)



# @connectdb
# def film_reviews(request, cursor, film_id):
#     # if 'username' not in request.COOKIES:
#     #     return redirect(reverse('authentication:login'))

#     # Fetch film details
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis
#         FROM pacilflix.tayangan t
#         WHERE t.id = %s
#     """, [film_id])
#     film = cursor.fetchone()

#     if not film:
#         return render(request, 'film_detail.html', {'error': 'Film not found'})

#     # Fetch reviews
#     cursor.execute("""
#         SELECT u.username, u.deskripsi, u.rating, u.timestamp
#         FROM pacilflix.ulasan u
#         WHERE u.id_tayangan = %s
#         ORDER BY u.timestamp DESC
#     """, [film_id])
#     reviews = cursor.fetchall()
#     context = {
#         'film': {
#             'id': film_id,
#             'judul': film[0],
#             'sinopsis': film[1],
#         },
#         'reviews': reviews
#     }
#     return render(request, 'film_reviews.html', context)

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

    # Fetch episode links
    cursor.execute("""
        SELECT e.sub_judul, e.url_video, e.release_date
        FROM pacilflix.episode e
        WHERE e.id_series = %s
    """, [series_id])
    episodes = cursor.fetchall()

    # Fetch average rating
    cursor.execute("""
        SELECT COALESCE(AVG(u.rating), 0)
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
    """, [series_id])
    rating_avg = cursor.fetchone()[0]

    # Fetch genres
    cursor.execute("""
        SELECT gt.genre
        FROM pacilflix.genre_tayangan gt
        WHERE gt.id_tayangan = %s
    """, [series_id])
    genres = cursor.fetchall()

    # Fetch players
    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.memainkan_tayangan mt
        JOIN pacilflix.contributors c ON mt.id_pemain = c.id
        WHERE mt.id_tayangan = %s
    """, [series_id])
    players = cursor.fetchall()

    # Fetch screenwriters
    cursor.execute("""
        SELECT c.nama
        FROM pacilflix.menulis_skenario_tayangan mst
        JOIN pacilflix.contributors c ON mst.id_penulis_skenario = c.id
        WHERE mst.id_tayangan = %s
    """, [series_id])
    screenwriters = cursor.fetchall()

    # Fetch director
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

    series_data = {
        'judul': series[0],
        'sinopsis': series[1],
        'url_video_trailer': series[2],
        'release_date_trailer': series[3],
        'asal_negara': series[4],
        'id_tayangan': series[5],
        'rating_avg': rating_avg,
        'episodes': [{'sub_judul': episode[0], 'url_video': episode[1], 'release_date': episode[2]} for episode in episodes],
        'genres': [genre[0] for genre in genres],
        'players': [player[0] for player in players],
        'screenwriters': [screenwriter[0] for screenwriter in screenwriters],
        'director': director[0] if director else None,
    }

    context = {
        'series': series_data
    }
    return render(request, 'series_detail.html', context)




@connectdb
def film_reviews(request, cursor, film_id):
    # Fetch film details
    cursor.execute("""
        SELECT judul, sinopsis
        FROM pacilflix.tayangan
        WHERE id = %s
    """, [film_id])
    film = cursor.fetchone()

    if not film:
        return render(request, 'film_detail.html', {'error': 'Film not found'})

    # Fetch reviews
    cursor.execute("""
        SELECT u.username, u.deskripsi, u.rating, u.timestamp
        FROM pacilflix.ulasan u
        WHERE u.id_tayangan = %s
        ORDER BY u.timestamp DESC
    """, [film_id])
    reviews = cursor.fetchall()

    context = {
        'film': {
            'id': film_id,
            'judul': film[0],
            'sinopsis': film[1],
        },
        'reviews': reviews
    }
    return render(request, 'film_reviews.html', context)

@connectdb
def add_review(request, cursor, film_id):
    # if 'username' not in request.COOKIES:
    #     return redirect(reverse('authentication:login'))

    if request.method == 'POST':
        username = request.COOKIES['username']
        deskripsi = request.POST['deskripsi']
        rating = request.POST['rating']
        timestamp = timezone.now()

        cursor.execute("""
            INSERT INTO pacilflix.ulasan (id_tayangan, username, timestamp, rating, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
        """, [film_id, username, timestamp, rating, deskripsi])

        return redirect(reverse('film_reviews', args=[film_id]))

    return redirect(reverse('film_reviews', args=[film_id]))


# @connectdb
# def get_trailers(cursor: CursorWrapper, request):
#     # Query untuk mendapatkan trailer film
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer 
#         FROM pacilflix.tayangan AS t 
#         JOIN pacilflix.film AS f ON t.id = f.id_tayangan
#     """)
#     film_list = cursor.fetchall()

#     # Query untuk mendapatkan trailer series
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer 
#         FROM pacilflix.tayangan AS t 
#         JOIN pacilflix.series AS s ON t.id = s.id_tayangan
#     """)
#     series_list = cursor.fetchall()
    
#     # Menggabungkan trailer film dan series dalam satu variabel HTML
#     trailers_html = "<h1>Daftar Trailer Film</h1>"
#     trailers_html += "<table border='1'><tr><th>Judul</th><th>Sinopsis</th><th>Trailer</th><th>Tanggal Rilis</th></tr>"
#     for film in film_list:
#         trailers_html += f"<tr><td>{film[0]}</td><td>{film[1]}</td><td><a href='{film[2]}'>Tonton Trailer</a></td><td>{film[3]}</td></tr>"
#     trailers_html += "</table>"
    
#     trailers_html += "<h1>Daftar Trailer Series</h1>"
#     trailers_html += "<table border='1'><tr><th>Judul</th><th>Sinopsis</th><th>Trailer</th><th>Tanggal Rilis</th></tr>"
#     for series in series_list:
#         trailers_html += f"<tr><td>{series[0]}</td><td>{series[1]}</td><td><a href='{series[2]}'>Tonton Trailer</a></td><td>{series[3]}</td></tr>"
#     trailers_html += "</table>"
    
#     return HttpResponse(trailers_html)



# def get_trailers(request):
#     # Anda mendapatkan daftar trailer dari database atau dari mana pun
#     tayangan_list = [...]  # Misalnya daftar ini diperoleh dari database
    
#     return render(request, 'trailers.html', {'tayangan_list': tayangan_list})
