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
# # def trailer_home(request):
# #     return render(request, "trailer_home.html")

# def connectdb(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         with connection.cursor() as cursor:
#             return func(request, cursor, *args, **kwargs)
        
# @connectdb
# def get_trailers(request, cursor):
#     # Query untuk mendapatkan trailer film
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
#         FROM pacilflix.tayangan AS t 
#         JOIN pacilflix.film AS f ON t.id = f.id_tayangan
#     """)
#     film_list = cursor.fetchall()

#     # Query untuk mendapatkan trailer series
#     cursor.execute("""
#         SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer 
#         FROM pacilflix.tayangan AS t 
#         JOIN pacilflix.series AS s ON t.id = s.id_tayangan
#     """)
#     series_list = cursor.fetchall()
    
#     # Tanggal sekarang
#     today = datetime.date.today()
#     # Tanggal 7 hari yang lalu
#     seven_days_ago = today - datetime.timedelta(days=7)

#     # Query untuk mendapatkan top 10 tayangan berdasarkan jumlah viewer dalam 7 hari terakhir
#     cursor.execute("""
#         SELECT
#             ROW_NUMBER() OVER (ORDER BY SUM(view_count) DESC) AS "Peringkat",
#             judul AS "Judul",
#             sinopsis_trailer AS "Sinopsis Trailer",
#             url_video_trailer AS "URL Trailer",
#             release_date_trailer AS "Tanggal Rilis Trailer",
#             SUM(view_count) AS "Total View 7 Hari Terakhir"
#         FROM (
#             SELECT
#                 T.id,
#                 T.judul,
#                 T.sinopsis_trailer,
#                 T.url_video_trailer,
#                 T.release_date_trailer,
#                 CASE
#                     WHEN RN.end_date_time >= RN.start_date_time + (F.durasi_film * INTERVAL '1 minute' * 0.70)
#                         AND RN.start_date_time BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
#                         THEN 1
#                     ELSE 0
#                 END AS view_count
#             FROM pacilflix.tayangan AS T
#             JOIN pacilflix.riwayat_nonton AS RN ON T.id = RN.id_tayangan
#             LEFT JOIN pacilflix.film AS F ON T.id = F.id_tayangan
#             UNION ALL
#             SELECT
#                 T.id,
#                 T.judul,
#                 T.sinopsis_trailer,
#                 T.url_video_trailer,
#                 T.release_date_trailer,
#                 CASE
#                     WHEN RN.end_date_time >= RN.start_date_time + (E.durasi * INTERVAL '1 minute' * 0.70)
#                         AND RN.start_date_time BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
#                         THEN 1
#                     ELSE 0
#                 END AS view_count
#             FROM pacilflix.tayangan AS T
#             JOIN pacilflix.series AS S ON T.id = S.id_tayangan
#             JOIN pacilflix.episode AS E ON S.id_tayangan = E.id_series
#             JOIN pacilflix.riwayat_nonton AS RN ON E.id_series = RN.id_tayangan
#         ) AS Combined
#         GROUP BY judul, sinopsis_trailer, url_video_trailer, release_date_trailer
#         ORDER BY "Total View 7 Hari Terakhir" DESC
#         LIMIT 10;
#     """)

#     top_10_trailers = cursor.fetchall()

#     return render(request, 'trailers.html', {
#         'film_list': film_list,
#         'series_list': series_list,
#         'top_10_trailers': top_10_trailers
#     })


# @connectdb
# def search_trailer(request, cursor):  # Tambahkan request di sini
#     query = request.GET.get('q')
#     search_results = []

#     if query:
#         try:
#             # Lakukan pencarian tayangan berdasarkan judul menggunakan SQL
#             cursor.execute("""
#                 SELECT judul, sinopsis_trailer, url_video_trailer, release_date_trailer
#                 FROM pacilflix.tayangan
#                 WHERE judul ILIKE %s
#             """, ['%' + query + '%'])

#             search_results = cursor.fetchall()
#         except OperationalError as e:
#             # Tangani kesalahan koneksi atau query
#             print(f"Error: {e}")
#             # Atau tampilkan pesan kesalahan ke pengguna

#     return render(request, 'trailers.html', {'search_results': search_results})

from django.shortcuts import render
from django.db import connection
from functools import wraps
import datetime
from django.http import HttpResponse

def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        with connection.cursor() as cursor:
            return func(request, cursor, *args, **kwargs)
    return wrapper

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
def search_trailer(request, cursor):
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
