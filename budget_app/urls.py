from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('test_base/', views.test_base, name = 'test_base'),
    path('add_budget/', views.add_budget, name='add_budget'),
    path('add_category/', views.add_category, name = 'add_category'),
    path('edit_category/', views.edit_category, name = 'edit_category'),
    path('budgets/<int:budget_id>/', views.view_budget, name = 'view_budget')
]
