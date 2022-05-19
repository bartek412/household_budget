from cProfile import label
from django import forms
from django.forms import ModelForm
from .models import Budget, BudgetUser, ExpenseIncome, Category
from django.contrib.auth.models import User


class ExpenseIncomeForm(ModelForm):
    def __init__(self, budget_id, income=True, *args, **kwargs):
        super(ExpenseIncomeForm, self).__init__(*args, **kwargs)
        categories = Category.objects.filter(budget_id=budget_id)
        self.fields["category_id"].queryset = categories.filter(income=income)
        
    class Meta:
        model = ExpenseIncome
        fields = ["name", "category_id", "description", "date", "amount"]
        widgets = {
            'name' : forms.TextInput(attrs={"class":"form-control justify-content-start"}),
            'category_id':forms.Select(attrs={'class': "custom-select"}),
            'description':forms.Textarea(attrs={'class':"form-control"}),
            'date':forms.DateInput(attrs={'class':"form-control"}),
            'amount':forms.NumberInput(attrs={'class':"form-control"})
        }



class AddUserForm(forms.Form):
    name = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class':"form-control"}))
    write = forms.BooleanField(label='Write permision', required=False, widget=forms.CheckboxInput(attrs={'class':"form-control"}))
