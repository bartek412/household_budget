from django.shortcuts import render, HttpResponse
from os import path
from .forms import BudgetForm
from .models import BudgetUser, Budget, Category
from django.contrib.auth.models import User  # importowanie domyslej tabeli userow
from django.db.models import Q

base_path = path.join('budget_app', 'base.html')


# Create your views here.
def base(request):
    return render(request, "budget_app/base.html")


def home(request, base_path=base_path):
    return render(request, "budget_app/home.html", {'base_path': base_path})


def register(request, base_path=base_path):
    return render(request, "budget_app/register.html", {'base_path': base_path})


def test_base(request):
    return render(request, "budget_app/test_base.html")


def add_budget(request, base_path=base_path):
    form = BudgetForm(request.POST)
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BudgetForm()

    return render(request, "budget_app/add_budget.html", {'form': form, 'base_path': base_path})


def add_category(request, base_path=base_path):
    budgetUser_objects = BudgetUser.objects.filter(user_id=request.user.id)
    budget_ids = []
    for i in budgetUser_objects:
        budget_ids.append(i.budget_id)
    budgets = []
    for i in budget_ids:
        budgets.append(Budget.objects.get(id=i.id))

    parent_categories = Category.objects.all()[:2]

    if request.method == "POST":
        # w odpowiedz post zwracany jest slownik z wartosciami z forma-a z template'u 'add_category'
        # klucze w slowniku sa nazwami pol z template'u
        name = request.POST['name']
        description = request.POST['description']
        parent_id = request.POST['parent_id']
        budget_id = request.POST['budget_id']

        c = Category(name=name, description=description, parent_id=Category.objects.get(id=parent_id),
                     budget_id=Budget.objects.get(id=budget_id))
        c.save()

    return render(request, "budget_app/add_category.html", {'base_path': base_path,
                                                            'budgets': budgets, 'parent_categories': parent_categories})


def edit_category(request, base_path=base_path):
    # pobranie kategorii ze wszystkich budzetow w ktorych uzytkownik posiada prawa edycji
    budgets = BudgetUser.objects.filter(user_id=request.user.id, role=1)  # zakładam, że 1 oznacza mozliwosc edycji
    categories = []
    for i in budgets:
        for j in Category.objects.filter(budget_id=i.budget_id): # kategorie bez parent_id
            categories.append(j)
    categories = categories[2:]  # dwie pierwsze kategorie to Expense i Income

    if request.method == "POST":
        category = Category.objects.get(id=request.POST['category'])
        if request.POST['name'] != '' or request.POST['name'] != category.name:
            category.name = request.POST['name']
        if request.POST['description'] != '' or request.POST['description'] != category.description:
            category.description = request.POST['description']
        category.save()

    return render(request, "budget_app/edit_category.html", {'base_path': base_path, 'categories': categories})


# Funkcja dodająca budżet z formularza
def add_budget(request, base_path=base_path):


    # Tablica z id userów, którzy są zapisani w bazie
    # users_ids = []
    # for i in budgetUser_objects:
    #     users_ids.append(i.user_id)

    users_objects = User.objects.all()
    users = []
    for i in users_objects:
        users.append(i.username)

    if request.method == "POST":
        # w odpowiedz post zwracany jest slownik z wartosciami z forma-a z template'u 'add_category'
        # klucze w slowniku sa nazwami pol z template'u
        name = request.POST['name']
        description = request.POST['description']
        user = request.POST['user']
        #print(name, description, user_id)

        # Dodanie nazwy budzetu i opisu do tabeli Budget
        b = Budget(name=name, description=description)
        b.save()

        u = User.objects.get(username=user)
        u.save()

        budget_quantity = len(Budget.objects.all())-1
        # Dodanie nazwy budzetu i opisu do tabeli Budget
        # bu = BudgetUser(user_id=User(username=user), budget_id=Budget.objects.all()[budget_quantity], role=1)
        # bu = BudgetUser(user_id=User(username=user), budget_id=Budget.objects.all()[1], role=1)
        bu = BudgetUser(user_id=u, budget_id=b, role=1)
        bu.save()

    return render(request, "budget_app/add_budget.html", {'base_path': base_path,
                                                          'users': users})
