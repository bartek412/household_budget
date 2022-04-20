from django import forms
from django.forms import ModelForm
from .models import Budget, BudgetUser, ExpenseIncome, Category
from django.contrib.auth.models import User


class ExpenseIncomeForm(ModelForm):
    def __init__(self, budget_id, *args, **kwargs):
        super(ExpenseIncomeForm, self).__init__(*args, **kwargs)
        self.fields["category_id"].queryset = Category.objects.filter(
            budget_id=budget_id
        )

    class Meta:
        model = ExpenseIncome
        fields = ["name", "category_id", "description", "date", "amount"]
