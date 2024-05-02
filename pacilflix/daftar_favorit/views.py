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

    return render(request, "main.html", context)

def create_product(request):
    form = data_daftar_favorit(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('daftar_favorit:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)