from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
import budget_app.models


class Budget(models.Model):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="BudgetUser")
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    parent_id = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_income_category(self):
        category = self
        while True:
            if category.parent_id is None:
                break
            else:
                category = Category.objects.get(id=category.parent_id.id)
        return True if category.name == 'Income' else False


class BudgetUser(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)
    role = models.IntegerField()


class ExpenseIncome(models.Model):
    name = models.CharField(max_length=30)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
