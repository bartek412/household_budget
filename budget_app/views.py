from django.shortcuts import render, HttpResponse
from os import path
from .forms import BudgetForm

base_path = path.join('budget_app', 'base.html')

# Create your views here.
def base(request):
    return render(request, "budget_app/base.html")


def home(request, base_path = base_path):
    return render(request, "budget_app/home.html",{'base_path':base_path})


def register(request, base_path = base_path):
    return render(request, "budget_app/register.html",{'base_path':base_path})

def test_base(request):
    return render(request, "budget_app/test_base.html")

def add_budget(request, base_path = base_path):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BudgetForm()
  
    return render(request, "budget_app/add_budget.html", {'form': form, 'base_path': base_path})