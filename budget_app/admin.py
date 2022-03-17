from django.contrib import admin
from django.conf import settings
from .models import Category, BudgetUser, Budget, ExpenseIncome

# Register your models here.
admin.site.register(Category)
admin.site.register(BudgetUser)
admin.site.register(Budget)
admin.site.register(ExpenseIncome)
