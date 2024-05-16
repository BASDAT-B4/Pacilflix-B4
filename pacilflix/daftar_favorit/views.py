from django.shortcuts import render
from django.http import HttpResponseRedirect
from daftar_favorit.forms import data_daftar_favorit
from django.urls import reverse
from daftar_favorit.models import data_daftar_favorit


def show_main(request):
    data = data_daftar_favorit.objects.all()

    context = {
        'name': 'Pak Bepe', # Nama kamu
        'class': 'PBP A', # Kelas PBP kamu
        'products': data
    }

    return render(request, "daftar_favorit.html", context)
