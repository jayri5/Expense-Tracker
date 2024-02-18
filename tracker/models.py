# models.py
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    
@receiver(post_save, sender=Expense)
def check_category_expenses(sender, instance, **kwargs):
    # Check if total expenses for the category exceed a fixed amount (e.g., 500)
    fixed_amount = 500  # Adjust this value as needed
    total_amount = Expense.objects.filter(user=instance.user, category=instance.category).aggregate(models.Sum('amount'))['amount__sum'] or 0

    if total_amount > fixed_amount:
        # You can implement the notification logic here (e.g., send an email, create a notification record)
        print(f"Warning: Total expenses for category '{instance.category}' exceeded {fixed_amount}. Current total: {total_amount}")


class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
