from django.shortcuts import render
from django.db import connection
from django.db.backends.utils import CursorWrapper



def connectdb(func):
    def wrapper(request):
        with connection.cursor() as cursor:
            return func(cursor, request)
    return wrapper

@connectdb
def trailer_home(cursor: CursorWrapper, request):
    with connection.cursor() as cursor:
        query = """
        SELECT 
            t.id,
            t.judul,
            t.sinopsis,
            t.url_video_trailer,
            t.release_date_trailer,
            COUNT(rn.username) AS total_view
        FROM 
            pacilflix.TAYANGAN AS t
        JOIN 
            pacilflix.RIWAYAT_NONTON rn ON t.id = rn.id_tayangan
        JOIN 
            pacilflix.FILM f ON t.id = f.id_tayangan
        WHERE 
            EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60 >= f.durasi_film * 0.7
            AND rn.start_date_time >= NOW() - INTERVAL '7 DAYS'
        GROUP BY 
            t.id, t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer
        ORDER BY 
            total_view DESC
        LIMIT 10;
        """
        cursor.execute(query)
        top_tayangan = cursor.fetchall()

    context = {
        'top_tayangan': [
            {
                'id': row[0],
                'judul': row[1],
                'sinopsis': row[2],
                'url_trailer': row[3],
                'tanggal_rilis': row[4],
                'total_view': row[5]
            }
            for row in top_tayangan
        ]
    }

    return render(request, 'trailer_home.html', context)
