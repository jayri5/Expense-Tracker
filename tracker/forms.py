# forms.py
from django import forms
from .models import Expense, Budget, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']