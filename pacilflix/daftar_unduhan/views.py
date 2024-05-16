from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, "daftar_unduhan.html", context)
