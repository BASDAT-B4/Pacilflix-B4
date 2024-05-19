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


# def get_daftar_unduhan(username):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT t.id_tayangan, t.username, t.timestamp, j.judul FROM pacilflix.tayangan_terunduh AS t JOIN pacilflix.tayangan AS j ON t.id_tayangan = j.id WHERE t.username = %s", [username])
#         columns = [col[0] for col in cursor.description]
#         return [
#             dict(zip(columns, row))
#             for row in cursor.fetchall()
#         ]



import datetime

def get_daftar_unduhan(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT t.id_tayangan, t.username, t.timestamp, j.judul FROM pacilflix.tayangan_terunduh AS t JOIN pacilflix.tayangan AS j ON t.id_tayangan = j.id WHERE t.username = %s", [username])
        columns = [col[0] for col in cursor.description]
        unduhan_list = []
        for row in cursor.fetchall():
            unduhan = dict(zip(columns, row))
            # Periksa jika timestamp kurang dari 1 hari
            timestamp = unduhan.get('timestamp')
            if timestamp:
                kurang_dari_1_hari = (datetime.datetime.now() - timestamp).days < 1
                unduhan['kurang_dari_1_hari'] = kurang_dari_1_hari
            unduhan_list.append(unduhan)
        return unduhan_list
