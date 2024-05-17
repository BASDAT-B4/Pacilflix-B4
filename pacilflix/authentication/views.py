from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.backends.utils import CursorWrapper
from .queries import AuthenticationManager

from django.urls import reverse

import datetime



def connectdb(func):
    def wrapper(request):
        with connection.cursor() as cursor:
            return func(cursor, request)
    return wrapper


def show_main(request):
    return render(request, "home.html")

@connectdb
def register(sql: CursorWrapper, request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara = request.POST.get('negara')

        with connection.cursor() as sql:
            sql.execute(AuthenticationManager.check_username(username), [username])
            existing_users = sql.fetchall()

            if existing_users:
                messages.error(request, "The username you chose is already in use.")
                return render(request, 'register.html', {'form': request.POST})

            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return render(request, 'register.html', {'form': request.POST})

            sql.execute(AuthenticationManager.insert_user(), [username, password, negara])
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login')

    return render(request, 'register.html')

@connectdb
def login_user(cursor: CursorWrapper, request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use the method from AuthenticationManager to get the SQL query
        cursor.execute(AuthenticationManager.check_user(), [username, password])
        users = cursor.fetchall()

        if users:
            request.session['username'] = username
            response = redirect('langganan:kelola_langganan')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('authentication:login_user')


def home(request):
    return render(request, "tayangan.html")