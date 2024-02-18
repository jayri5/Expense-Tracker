# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category, Budget
from .forms import ExpenseForm, BudgetForm, CategoryForm
from django.db import models
from datetime import date
import calendar

@login_required
def expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses.html', {'expenses': expenses})

@login_required
def submit_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses')
    else:
        form = ExpenseForm()
    return render(request, 'submit_expense.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

'''
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Expense, Category, Budget
from .forms import ExpenseForm, BudgetForm, CategoryForm
import calendar
from datetime import date, timedelta


def expense_summary(request):
    categories = Category.objects.all()
    summary = {}
    
    # Retrieve the selected time period and month from the request parameters
    time_period = request.GET.get('time_period', 'monthly')
    selected_month = int(request.GET.get('selected_month', date.today().month))

    # Calculate start and end dates based on the selected time period and month
    today = date.today()
    if time_period == 'daily':
        start_date = today
        end_date = today
    elif time_period == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif time_period == 'monthly':
        start_date = today.replace(year=today.year, month=selected_month, day=1)
        end_date = today.replace(year=today.year, month=selected_month, day=calendar.monthrange(today.year, selected_month)[1])
    elif time_period == 'quarterly':
        start_date = today.replace(month=((today.month - 1) // 3) * 3 + 1, day=1)
        end_date = start_date.replace(month=start_date.month + 2, day=calendar.monthrange(today.year, start_date.month + 2)[1])
    elif time_period == 'yearly':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)

    # Precompute month options for the dropdown
    month_options = [(month_num, calendar.month_name[month_num]) for month_num in range(1, 13)]

    # Retrieve expense data for each category within the specified time period
    for category in categories:
        total_amount = Expense.objects.filter(user=request.user, category=category, date__range=(start_date, end_date)).aggregate(models.Sum('amount'))['amount__sum'] or 0
        summary[category.name] = total_amount

    return render(request, 'expense_summary.html', {'summary': summary, 'time_period': time_period, 'selected_month': selected_month, 'month_options': month_options})
'''

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Expense, Category, Budget
from .forms import ExpenseForm, BudgetForm, CategoryForm
import calendar
from datetime import date, timedelta

@login_required
def expense_summary(request):
    categories = Category.objects.all()
    summary = {}
    
    # Retrieve the selected time period and month from the request parameters
    time_period = request.GET.get('time_period', 'monthly')
    selected_month = int(request.GET.get('selected_month', date.today().month))
    selected_year = int(request.GET.get('selected_year', date.today().year))  # Add this line to retrieve selected year

    # Calculate start and end dates based on the selected time period, month, and year
    today = date.today()
    if time_period == 'daily':
        start_date = today
        end_date = today
    elif time_period == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif time_period == 'monthly':
        start_date = today.replace(year=selected_year, month=selected_month, day=1)
        end_date = today.replace(year=selected_year, month=selected_month, day=calendar.monthrange(selected_year, selected_month)[1])
    elif time_period == 'quarterly':
        start_date = today.replace(month=((today.month - 1) // 3) * 3 + 1, day=1)
        end_date = start_date.replace(month=start_date.month + 2, day=calendar.monthrange(today.year, start_date.month + 2)[1])
    elif time_period == 'yearly':
        start_date = today.replace(year=selected_year, month=1, day=1)  # Update to include selected year
        end_date = today.replace(year=selected_year, month=12, day=31)  # Update to include selected year

    # Precompute month options for the dropdown
    month_options = [(month_num, calendar.month_name[month_num]) for month_num in range(1, 13)]

    # Precompute year options for the dropdown
    year_options = [year for year in range(2018, date.today().year + 1)]  # Generate years from 2018 to current year

    # Retrieve expense data for each category within the specified time period
    for category in categories:
        total_amount = Expense.objects.filter(user=request.user, category=category, date__range=(start_date, end_date)).aggregate(models.Sum('amount'))['amount__sum'] or 0
        summary[category.name] = total_amount

    return render(request, 'expense_summary.html', {'summary': summary, 'time_period': time_period, 'selected_month': selected_month, 'month_options': month_options, 'selected_year': selected_year, 'year_options': year_options})


@login_required
def manage_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('manage_budget')
    else:
        form = BudgetForm()
    
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'manage_budget.html', {'form': form, 'budgets': budgets})
