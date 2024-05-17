from django.urls import path
from langganan.views import *

app_name = 'kelola_langganan'

urlpatterns = [
    path('kelola_langganan/', show_cru_langganan, name='kelola_langganan'),
    path('beli_paket/<str:nama_paket>/<str:param>/', show_payment_confirmation, name='beli_paket'),
    path('beli/<str:nama_paket>/<str:metode_pembayaran>/', purchase_package, name='beli'),
]