from django.shortcuts import render

def trailer_home(request):
    return render(request, "trailer_home.html")