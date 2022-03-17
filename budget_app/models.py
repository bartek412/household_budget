from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
import budget_app.models


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)


class Budget(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BudgetUser')


class BudgetUser(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)


class ExpenseIncome(models.Model):
    name = models.CharField(max_length=30)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)
