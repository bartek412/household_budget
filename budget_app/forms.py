from django import forms
from django.forms import ModelForm
from .models import Budget, BudgetUser, ExpenseIncome, Category
from django.contrib.auth.models import User


class ExpenseIncomeForm(ModelForm):
    def __init__(self, budget_id, income=True, *args, **kwargs):
        super(ExpenseIncomeForm, self).__init__(*args, **kwargs)
        categories = Category.objects.filter(budget_id=budget_id)
        main_category = categories.filter(
            name='Income' if income else 'Expense')
        self.fields["category_id"].queryset = main_category | categories.filter(
            parent_id=main_category[0])

    class Meta:
        model = ExpenseIncome
        fields = ["name", "category_id", "description", "date", "amount"]
