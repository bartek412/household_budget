from django.shortcuts import render, HttpResponse
from os import path

base_path = path.join('budget_app', 'base.html')

# Create your views here.
def base(request):
    return render(request, "budget_app/base.html")


def home(request, base_path = base_path):
    return render(request, "budget_app/home.html",{'base_path':base_path})


def register(request, base_path = base_path):
    return render(request, "budget_app/register.html",{'base_path':base_path})
