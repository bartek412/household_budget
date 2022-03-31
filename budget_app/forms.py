#from django import forms
from django.forms import ModelForm
from .models import Budget


# class BudgetForm(forms.ModelForm):
#     class Meta:
#         model = Budget
#         fields = [
#             'name', 'users'
#         ]

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = [
            'name', 'users'
        ]
