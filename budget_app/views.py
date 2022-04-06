from django.shortcuts import render, HttpResponse
from os import path
from .forms import BudgetForm
from .models import BudgetUser

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
    form = BudgetForm(request.POST)
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BudgetForm()

    return render(request, "budget_app/add_budget.html", {'form': form, 'base_path': base_path})



def add_category(request, base_path = base_path):

    budgetUser_objects = BudgetUser.objects.get(user_id = request.user.id)
    budget_ids = []
    for i in budgetUser_objects:
        budget_ids.append(i.budget_id)

    if request.method == "POST":
        pass

    return render(request, "budget_app/add_category.html", {'base_path': base_path, 'budget_ids' : budget_ids})
    