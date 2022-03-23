from django.shortcuts import render, HttpResponse


# Create your views here.
def base(request):
    return render(request, 'budget_app/base.html')
def home(request):
    return render(request, 'budget_app/home.html')
def register(request):
    return render(request, 'budget_app/register.html')