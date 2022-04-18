from django.shortcuts import render, HttpResponse
from os import path

from psutil import users
from .forms import BudgetForm
from .models import BudgetUser, Budget, Category
from django.contrib.auth.models import User  # importowanie domyslej tabeli userow
from django.db.models import Q
from enum import Enum
from django.contrib.auth.decorators import login_required


Role = Enum('Role', 'OWNER EDIT VIEW')

base_path = path.join('budget_app', 'base.html')
budget_base_path = path.join('budget_app', 'view_budget.html')

def get_budget_list(request):
    budgetUser_objects = BudgetUser.objects.filter(user_id=request.user.id)
    budget_ids = []
    for i in budgetUser_objects:
        budget_ids.append(i.budget_id)
    budgets_list = [Budget.objects.get(id = i.budget_id.id) for i in budgetUser_objects]
    return budgets_list

def if_can_edit(budget_id, request):
    role = BudgetUser.objects.get(budget_id = budget_id, user_id = request.user.id).role
    if Role(role).name == "OWNER" or Role(role).name == "EDIT":
        return True
    else:
        return False

@login_required(login_url='login')
# Create your views here.
def base(request):
    budgets_list = get_budget_list(request)
    return render(request, "budget_app/base.html", {'budgets_list': budgets_list})

@login_required(login_url='login')
def home(request, base_path=base_path):
    return render(request, "budget_app/home.html", {'base_path': base_path})

@login_required(login_url='login')
def register(request, base_path=base_path):
    return render(request, "budget_app/register.html", {'base_path': base_path})

@login_required(login_url='login')
def test_base(request):
    return render(request, "budget_app/test_base.html")

@login_required(login_url='login')
def add_budget(request, base_path=base_path):
    form = BudgetForm(request.POST)
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BudgetForm()

    return render(request, "budget_app/add_budget.html", {'form': form, 'base_path': base_path})

@login_required(login_url='login')
def add_category(request, budget_id, base_path=base_path, budget_base_path=budget_base_path):
    parent_categories = Category.objects.filter(budget_id = budget_id)
    if request.method == "POST":
        # w odpowiedz post zwracany jest slownik z wartosciami z forma-a z template'u 'add_category'
        # klucze w slowniku sa nazwami pol z template'u
        name = request.POST['name']
        description = request.POST['description']
        parent_id = request.POST['parent_id']
        c = Category(name=name, description=description, parent_id=Category.objects.get(id=parent_id),
                     budget_id=Budget.objects.get(id=budget_id))
        c.save()
    budgets_list = get_budget_list(request)
    categories = Category.objects.filter(budget_id = budget_id)
    owner_or_edit = if_can_edit(budget_id, request)
    budget = Budget.objects.get(id = budget_id)
    return render(request, "budget_app/add_category.html", {'base_path': base_path,
                                                            'parent_categories': parent_categories,
                                                            'budget_base_path': budget_base_path,
                                                            'budgets_list':budgets_list,
                                                            'categories':categories,
                                                            'owner_or_edit':owner_or_edit,
                                                            'budget':budget})

@login_required(login_url='login')
def edit_category(request, budget_id, category_id, base_path=base_path, budget_base_path =  budget_base_path,):

    if request.method == "POST":
        category = Category.objects.get(id=category_id)
        if request.POST['name'] != '' or request.POST['name'] != category.name:
            category.name = request.POST['name']
        if request.POST['description'] != '' or request.POST['description'] != category.description:
            category.description = request.POST['description']
        category.save()
    budgets_list = get_budget_list(request)
    categories = Category.objects.filter(budget_id = budget_id)
    owner_or_edit = if_can_edit(budget_id, request)
    budget = Budget.objects.get(id = budget_id)
    category = Category.objects.get(id = category_id)
    parent = Category.objects.get(id = category.parent_id.id)
    return render(request, "budget_app/edit_category.html", {'base_path': base_path, 
                                                            'categories': categories,
                                                            'budget_base_path': budget_base_path,
                                                            'budgets_list':budgets_list,
                                                            'owner_or_edit': owner_or_edit,
                                                            'budget':budget,
                                                            'category':category,
                                                            'parent':parent
                                                            })
@login_required(login_url='login')
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
        users_list = request.POST.getlist('users_list')
        print(name, description, users_list)

        # Dodanie nazwy budzetu i opisu do tabeli Budget
        b = Budget(name=name, description=description)
        b.save()

        for user in users_list:
            u = User.objects.get(username=user)
            # u.save()

            budget_quantity = len(Budget.objects.all())-1
            # Dodanie nazwy budzetu i opisu do tabeli Budget
            # bu = BudgetUser(user_id=User(username=user), budget_id=Budget.objects.all()[budget_quantity], role=1)
            # bu = BudgetUser(user_id=User(username=user), budget_id=Budget.objects.all()[1], role=1)
            bu = BudgetUser(user_id=u, budget_id=b, role=1)
            bu.save()
    budgets_list = get_budget_list(request)
    return render(request, "budget_app/add_budget.html", {'base_path': base_path,
                                                          'users': users,
                                                          'budgets_list': budgets_list,
                                                          })
@login_required(login_url='login')
def view_budget(request, budget_id, base_path=base_path):
    budgets_list = get_budget_list(request)
    budget = Budget.objects.get(id = budget_id)
    categories = Category.objects.filter(budget_id = budget_id)
    owner_or_edit = if_can_edit(budget_id, request)
    return render(request, "budget_app/view_budget.html", {'budget': budget, 
                                                            'base_path':base_path,
                                                            'budgets_list': budgets_list,
                                                            'categories': categories,
                                                            'owner_or_edit': owner_or_edit})
@login_required(login_url='login')
def view_category(request, budget_id, category_id, base_path = base_path):
    budget = Budget.objects.get(id = budget_id)
    budgets_list = get_budget_list(request)
    categories = Category.objects.filter(budget_id = budget_id)
    category = Category.objects.get(id = category_id)
    owner_or_edit = if_can_edit(budget_id, request)
    return render(request, "budget_app/view_category.html", {'category':category,
                                                            'base_path': base_path,
                                                            'budgets_list': budgets_list,
                                                            'categories': categories,
                                                            'owner_or_edit': owner_or_edit,
                                                            'budget':budget})



