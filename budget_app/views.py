import json

from django.shortcuts import redirect, render, HttpResponse
from os import path
import pandas as pd

from psutil import users
from .forms import ExpenseIncomeForm, AddUserForm
from .models import BudgetUser, Budget, Category, ExpenseIncome
# importowanie domyslej tabeli userow
from django.contrib.auth.models import User
from django.db.models import Q
from enum import Enum
from django.contrib import messages
from django.contrib.auth.decorators import login_required


Role = Enum("Role", "OWNER EDIT VIEW")

base_path = path.join("budget_app", "base.html")
budget_base_path = path.join("budget_app", "view_budget.html")


def get_budget_list(request):
    budgetUser_objects = BudgetUser.objects.filter(user_id=request.user.id)
    budget_ids = []
    for i in budgetUser_objects:
        budget_ids.append(i.budget_id)
    budgets_list = [Budget.objects.get(id=i.budget_id.id)
                    for i in budgetUser_objects]
    return budgets_list


def if_can_edit(budget_id, request):
    role = BudgetUser.objects.get(
        budget_id=budget_id, user_id=request.user.id).role
    if Role(role).name == "OWNER" or Role(role).name == "EDIT":
        return True
    else:
        return False


@login_required(login_url="login")
# Create your views here.
def base(request):
    budgets_list = get_budget_list(request)
    return render(request, "budget_app/base.html", {"budgets_list": budgets_list})


@login_required(login_url="login")
def home(request, base_path=base_path):
    budgets_list = get_budget_list(request)
    return render(request, "budget_app/home.html", {"base_path": base_path,
                                                    "budgets_list": budgets_list})


@login_required(login_url="login")
def register(request, base_path=base_path):
    return render(request, "budget_app/register.html", {"base_path": base_path})


@login_required(login_url="login")
def test_base(request):
    return render(request, "budget_app/test_base.html")


@login_required(login_url="login")
def add_category(
    request, budget_id, base_path=base_path, budget_base_path=budget_base_path
):
    parent_categories = Category.objects.filter(budget_id=budget_id)
    if request.method == "POST":
        # w odpowiedz post zwracany jest slownik z wartosciami z forma-a z template'u 'add_category'
        # klucze w slowniku sa nazwami pol z template'u
        name = request.POST["name"]
        description = request.POST["description"]
        parent_id = request.POST["parent_id"]
        income = Category.objects.get(id=parent_id).is_income_category()
        c = Category(
            name=name,
            description=description,
            parent_id=Category.objects.get(id=parent_id),
            budget_id=Budget.objects.get(id=budget_id),
            income=income
        )
        c.save()
        messages.success(request, 'Category added successfully')
    budgets_list = get_budget_list(request)
    categories = Category.objects.filter(budget_id=budget_id)
    owner_or_edit = if_can_edit(budget_id, request)
    budget = Budget.objects.get(id=budget_id)

    return render(
        request,
        "budget_app/add_category.html",
        {
            "base_path": base_path,
            "parent_categories": parent_categories,
            "budget_base_path": budget_base_path,
            "budgets_list": budgets_list,
            "categories": categories,
            "owner_or_edit": owner_or_edit,
            "budget": budget,
        },
    )


@login_required(login_url="login")
def edit_category(
    request,
    budget_id,
    category_id,
    base_path=base_path,
    budget_base_path=budget_base_path,
):

    if request.method == "POST":
        category = Category.objects.get(id=category_id)
        if request.POST["name"] != "" or request.POST["name"] != category.name:
            category.name = request.POST["name"]
        if (
            request.POST["description"] != ""
            or request.POST["description"] != category.description
        ):
            category.description = request.POST["description"]
        category.save()
        messages.success(request, 'Category edited successfully!')
    budgets_list = get_budget_list(request)
    categories = Category.objects.filter(budget_id=budget_id)
    owner_or_edit = if_can_edit(budget_id, request)
    budget = Budget.objects.get(id=budget_id)
    category = Category.objects.get(id=category_id)
    parent = Category.objects.get(id=category.parent_id.id)
    return render(
        request,
        "budget_app/edit_category.html",
        {
            "base_path": base_path,
            "categories": categories,
            "budget_base_path": budget_base_path,
            "budgets_list": budgets_list,
            "owner_or_edit": owner_or_edit,
            "budget": budget,
            "category": category,
            "parent": parent,
        },
    )


@login_required(login_url="login")
# Funkcja dodająca budżet z formularza
def add_budget(request, base_path=base_path):
    added = False
    # Tablica z id userów, którzy są zapisani w bazie
    # users_ids = []
    # for i in budgetUser_objects:
    #     users_ids.append(i.user_id)

    users_objects = User.objects.all()
    users = []
    for i in users_objects:
        users.append(i.username)

    if request.method == "POST":
        added = True
        # w odpowiedz post zwracany jest slownik z wartosciami z forma-a z template'u 'add_category'
        # klucze w slowniku sa nazwami pol z template'u
        name = request.POST["name"]
        description = request.POST["description"]
        users_list = request.POST.getlist("users_list")

        # Dodanie nazwy budzetu i opisu do tabeli Budget
        b = Budget(name=name, description=description)
        b.save()

        for user in users_list:
            u = User.objects.get(username=user)
            # u.save()

            budget_quantity = len(Budget.objects.all()) - 1
            # Dodanie nazwy budzetu i opisu do tabeli Budget
            # bu = BudgetUser(user_id=User(username=user), budget_id=Budget.objects.all()[budget_quantity], role=1)
            # bu = BudgetUser(user_id=User(username=user), budget_id=Budget.objects.all()[1], role=1)
            bu = BudgetUser(user_id=u, budget_id=b, role=1)
            bu.save()
        expense = Category(
            name="Expense",
            description="Base Expense",
            budget_id=b,
            income=False
        )
        expense.save()
        income = Category(
            name="Income",
            description="Base Income",
            budget_id=b,
        )
        income.save()
        messages.success(request, 'Budget added succesfully!')
        return redirect('/budgets/{}/'.format(b.id))
    budgets_list = get_budget_list(request)
    return render(
        request,
        "budget_app/add_budget.html",
        {
            "base_path": base_path,
            "users": users,
            "budgets_list": budgets_list,
            'added': added
        },
    )


@login_required(login_url="login")
def view_budget(request, budget_id, base_path=base_path):
    budgets_list = get_budget_list(request)
    budget = Budget.objects.get(id=budget_id)
    categories = Category.objects.filter(budget_id=budget_id)
    owner_or_edit = if_can_edit(budget_id, request)
    expenseincome = ExpenseIncome.objects.filter(budget_id=budget_id)
    expenseincome_json = pd.DataFrame(
        expenseincome).reset_index().to_json(orient='records')
    data = []
    data = json.loads(expenseincome_json)

    expenses = {'amount':[], 'category':[]}
    incomes = {'amount':[], 'category':[]}
    
    for i in expenseincome:
        if i.category_id.is_income_category():
            incomes['amount'].append(i.amount)
            incomes['category'].append(i.category_id.name)
        else:
            expenses['amount'].append(i.amount)
            expenses['category'].append(i.category_id.name)
    
    expenses = pd.DataFrame(expenses)
    incomes = pd.DataFrame(incomes)

    expenses = expenses.groupby('category').sum()
    incomes = incomes.groupby('category').sum()

    income_amt, income_cat = [float(i) for i in list(incomes['amount'].values)], list(incomes['amount'].keys())
    expense_amt, expense_cat = [float(i) for i in list(expenses['amount'].values)], list(expenses['amount'].keys())
    print(income_amt)
    print(income_cat)
    return render(
        request,
        "budget_app/view_budget.html",
        {
            "budget": budget,
            "base_path": base_path,
            "budgets_list": budgets_list,
            "categories": categories,
            "owner_or_edit": owner_or_edit,
            "expenseincome": expenseincome,
            "expenseincome_df": expenseincome_json,
            "d": data,
            "income_amt":income_amt,
            "income_cat":income_cat,
            "expense_amt":expense_amt,
            "expense_cat":expense_cat
        },
    )


@login_required(login_url="login")
def view_category(request, budget_id, category_id, base_path=base_path):
    budget = Budget.objects.get(id=budget_id)
    budgets_list = get_budget_list(request)
    categories = Category.objects.filter(budget_id=budget_id)
    category = Category.objects.get(id=category_id)
    owner_or_edit = if_can_edit(budget_id, request)
    return render(
        request,
        "budget_app/view_category.html",
        {
            "category": category,
            "base_path": base_path,
            "budgets_list": budgets_list,
            "categories": categories,
            "owner_or_edit": owner_or_edit,
            "budget": budget,
        },
    )


@login_required(login_url="login")
def add_income(
    request, budget_id, base_path=base_path, budget_base_path=budget_base_path
):
    form = ExpenseIncomeForm(budget_id, True, request.POST)
    if request.method == "POST":
        form = ExpenseIncomeForm(budget_id, True, request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            budget = Budget.objects.get(id=budget_id)
            income.budget_id = budget
            income.save()
            messages.success(request, "Income added successfully!")
            form = ExpenseIncomeForm(budget_id, True)
    else:
        form = ExpenseIncomeForm(budget_id=budget_id)
    budgets_list = get_budget_list(request)
    return render(
        request,
        "budget_app/form.html",
        {
            "form": form,
            "budget_id": budget_id,
            "budget_base_path": budget_base_path,
            "base_path": base_path,
            "budgets_list": budgets_list,
        },
    )


@login_required(login_url="login")
def add_expense(
    request, budget_id, base_path=base_path, budget_base_path=budget_base_path
):
    form = ExpenseIncomeForm(budget_id, False, request.POST)
    if request.method == "POST":
        form = ExpenseIncomeForm(budget_id, False, request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            budget = Budget.objects.get(id=budget_id)
            income.budget_id = budget
            income.save()
            messages.success(request, 'Expense added successfully!')
            form = ExpenseIncomeForm(budget_id, False)
    else:
        form = ExpenseIncomeForm(budget_id, False)
    budgets_list = get_budget_list(request)
    return render(
        request,
        "budget_app/form.html",
        {
            "form": form,
            "budget_id": budget_id,
            "budget_base_path": budget_base_path,
            "base_path": base_path,
            "budgets_list": budgets_list, })
# Dodawanie istniejacego uzytkownika do budzetu


@login_required(login_url="login")
def add_user(
    request, budget_id, base_path=base_path, budget_base_path=budget_base_path
):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            budget = Budget.objects.get(id=budget_id)
            try:
                user = User.objects.get(username=form.cleaned_data['name'])
            except User.DoesNotExist:
                user = None
                messages.error(
                    request, 'User not found')

            if user:
                permision = Role['EDIT'].value if form.cleaned_data['write'] else Role['VIEW'].value
                if not BudgetUser.objects.filter(user_id=user, budget_id=budget):
                    bu = BudgetUser(
                        user_id=user, budget_id=budget, role=permision)
                    bu.save()
                    messages.success(request, 'User added successfully!')
                else:
                    messages.error(
                        request, 'User is already added')
    else:
        form = AddUserForm()
    budgets_list = get_budget_list(request)
    return render(
        request,
        "budget_app/form.html",
        {"form": form,
            "base_path": base_path,
            "budget_base_path": budget_base_path,
            "budgets_list": budgets_list,
         },
    )
