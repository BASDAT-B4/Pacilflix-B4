from django.shortcuts import render, redirect
from django.db import connection
from langganan.query import *
from daftar_kontributor.utils.helper import *

# Create your views here.
def show_cru_langganan(request):
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()

    cursor1.execute(SubscriptionManager.get_active_package())
    cursor2.execute(SubscriptionManager.get_all_packages())
    cursor3.execute(SubscriptionManager.get_transaction_history())

    context = {
        'paket_langganan_aktif': EncodeHelper.toSQL(cursor1), 
        'daftar_paket': EncodeHelper.toSQL(cursor2), 
        'riwayat_transaksi': EncodeHelper.toSQL(cursor3)
    }

    return render(request, "cru_langganan.html", context)

def show_payment_confirmation(request, nama_paket, param='Transfer Bank'):
    cursor = connection.cursor()
    cursor.execute(SubscriptionManager.get_all_packages())
    daftar_paket = EncodeHelper.toSQL(cursor)

    paket = [paket for paket in daftar_paket if paket['nama'] == nama_paket]
    print(paket[0])

    return render(request, "beli_paket.html", {'paket': paket[0], 'param': param})

def purchase_package(request, nama_paket, metode_pembayaran):
    cursor = connection.cursor()
    cursor.execute(SubscriptionManager.purchase_package(nama_paket, metode_pembayaran))
    return redirect('langganan:kelola_langganan')