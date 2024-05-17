from django.shortcuts import render
from django.db import connection
from daftar_kontributor.query import ContributorManager
from daftar_kontributor.utils.helper import EncodeHelper
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponse, HttpResponseRedirect

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
def connectdb(func):
    def wrapper(request):
        with connection.cursor() as cursor:
            return func(cursor, request)
    return wrapper

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