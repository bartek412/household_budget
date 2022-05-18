from django import forms
from django.forms import ModelForm
from .models import Budget, BudgetUser, ExpenseIncome, Category
from django.contrib.auth.models import User


class ExpenseIncomeForm(ModelForm):
    def __init__(self, budget_id, income=True, *args, **kwargs):
        super(ExpenseIncomeForm, self).__init__(*args, **kwargs)
        categories = Category.objects.filter(budget_id=budget_id)
        print('xDDdDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
        print(categories.filter(income=income))
        self.fields["category_id"].queryset = categories.filter(income=income)

    class Meta:
        model = ExpenseIncome
        fields = ["name", "category_id", "description", "date", "amount"]


class AddUserForm(forms.Form):
    name = forms.CharField(label='Username', max_length=30)
    write = forms.BooleanField(label='write permision', required=False)
