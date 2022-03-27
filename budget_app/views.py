from django.shortcuts import render, HttpResponse
from .forms import BudgetForm


# Create your views here.
def base(request):
    return render(request, "budget_app/base.html")


def home(request):
    return render(request, "budget_app/home.html")


def register(request):
    return render(request, "budget_app/register.html")


def add_budget(request):
    return render(request, "budget_app/add_budget.html")


def BudgetFormView(request):
    form = BudgetForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "add_budget.html", context)
