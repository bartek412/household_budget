from turtle import home
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from os import path
# Create your views here.

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('login')  # po zarejestrowaniu przekierowanie na strone logowania
    else:
        form = RegisterForm()
    return render(response, 'register/register.html', {'form':form})

@login_required  #dekorator wymaga zalogowania przed przejsciem na strone 'profile'
def profile(response):
    return render(response, 'register/profile.html')