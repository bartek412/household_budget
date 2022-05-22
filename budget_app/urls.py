from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("test_base/", views.test_base, name="test_base"),
    path("add_budget/", views.add_budget, name="add_budget"),
    path(
        "budgets/<int:budget_id>/add_category/", views.add_category, name="add_category"
    ),
    path(
        "budgets/<int:budget_id>/category/<int:category_id>/edit/",
        views.edit_category,
        name="edit_category",
    ),
    path("budgets/<int:budget_id>/", views.view_budget, name="view_budget"),
    path(
        "budgets/<int:budget_id>/category/<int:category_id>/",
        views.view_category,
        name="view_category",
    ),
    path("budgets/<int:budget_id>/add_income/",
         views.add_income, name="add_income"),
    path("budgets/<int:budget_id>/add_expense/",
         views.add_expense, name="add_expense"),
    path("budgets/<int:budget_id>/add_income/",
         views.add_income, name="add_income"),
    path(
        "budgets/<int:budget_id>/add_user/", views.add_user, name="add_user"
    ),
  
]
