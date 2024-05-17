from django.db import connection

# def get_daftar_unduhan():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT t.id_tayangan, t.username, t.timestamp, j.judul FROM pacilflix.tayangan_terunduh AS t JOIN pacilflix.tayangan AS j ON t.id_tayangan = j.id")
#         columns = [col[0] for col in cursor.description]
#         return [
#             dict(zip(columns, row))
#             for row in cursor.fetchall()
#         ]
        
from django.db import connection

def get_daftar_unduhan(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT t.id_tayangan, t.username, t.timestamp, j.judul FROM pacilflix.tayangan_terunduh AS t JOIN pacilflix.tayangan AS j ON t.id_tayangan = j.id WHERE t.username = %s", [username])
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
