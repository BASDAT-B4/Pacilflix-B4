from django.shortcuts import render
from django.db import connection
from daftar_kontributor.query import ContributorManager
from daftar_kontributor.utils.helper import EncodeHelper
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponse, HttpResponseRedirect
from functools import wraps

# Create your views here.
def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        with connection.cursor() as cursor:
            return func(request, cursor, *args, **kwargs)
    return wrapper



@connectdb
def show_daftar_kontributor(request, cursor, tipe='all'):
    if tipe.lower() == 'all':
        cursor.execute(ContributorManager.get_all_contributors())
    elif tipe.lower() == 'sutradara':
        cursor.execute(ContributorManager.filter_by_sutradara())
    elif tipe.lower() == 'pemain':
        cursor.execute(ContributorManager.filter_by_pemain())
    elif tipe.lower() == 'penulis skenario':
        cursor.execute(ContributorManager.filter_by_penulis_skenario())
    
    contributors = EncodeHelper.toSQL(cursor)
    
    for contributor in contributors:
        contributor['jenis_kelamin'] = 'Laki-laki' if contributor['jenis_kelamin'] == 0 else 'Perempuan'

    return render(request, "list_kontributor.html", {'contributors': contributors, 'param': tipe})
