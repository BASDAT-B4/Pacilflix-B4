# from django.db import connection

# def get_daftar_favorit():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT judul, username, timestamp FROM pacilflix.daftar_favorit")
#         columns = [col[0] for col in cursor.description]
#         return [
#             dict(zip(columns, row))
#             for row in cursor.fetchall()
#         ]

from django.db import connection

def get_daftar_favorit(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT judul, username, timestamp FROM pacilflix.daftar_favorit WHERE username = %s", [username])
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


