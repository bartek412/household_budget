from django import forms
from django.forms import ModelForm
from .models import Budget, BudgetUser, ExpenseIncome
from django.contrib.auth.models import User


class BudgetForm(ModelForm):
    users = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=User.objects.all()
    )

    # role = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=BudgetUser.objects.all()
    # )
    class Meta:
        model = Budget
        fields = ["name", "description", "users"]


class ExpenseIncomeForm(ModelForm):
    class Meta:
        model = ExpenseIncome
        fields = ["name", "category_id", "description", "date", "amount"]
