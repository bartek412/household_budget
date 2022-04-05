from django.shortcuts import render, HttpResponse
from os import path
from .forms import BudgetForm
from .models import BudgetUser, Budget, Category
from django.db.models import Q


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

def add_category(request, base_path = base_path):

    budgetUser_objects = BudgetUser.objects.filter(user_id = request.user.id)
    budget_ids = []
    for i in budgetUser_objects:
        budget_ids.append(i.budget_id)
    budgets =[]
    for i in budget_ids:
        budgets.append(Budget.objects.get(id = i.id))

    parent_categories = Category.objects.all()[:2]

    if request.method == "POST":
        # w odpowiedz post zwracany jest slownik z wartosciami z forma-a z template'u 'add_category'
        # klucze w slowniku sa nazwami pol z template'u
        name = request.POST['name']
        description = request.POST['description']
        parent_id = request.POST['parent_id']
        budget_id = request.POST['budget_id']

        c = Category(name = name, description = description, parent_id = Category.objects.get(id = parent_id), 
                    budget_id = Budget.objects.get(id = budget_id))
        c.save()

    return render(request, "budget_app/add_category.html", {'base_path': base_path, 
    'budgets' : budgets,'parent_categories':parent_categories})
    