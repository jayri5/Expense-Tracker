# urls.py
from django.urls import path
from .views import expenses, submit_expense, expense_summary, manage_budget, create_category

urlpatterns = [
    path('', expenses, name='expenses'),
    path('expenses/', expenses, name='expenses'),
    path('submit_expense/', submit_expense, name='submit_expense'),
    path('expense_summary/', expense_summary, name='expense_summary'),
    path('manage_budget/', manage_budget, name='manage_budget'),
    path('create_category/', create_category, name='create_category'),
]
