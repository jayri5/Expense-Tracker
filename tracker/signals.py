# your_app_name/signals.py
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Expense
from django.db import models

@receiver(post_save, sender=Expense)
def check_category_expenses(sender, instance, **kwargs):
    fixed_amount = 500  # Adjust this value as needed
    total_amount = Expense.objects.filter(user=instance.user, category=instance.category).aggregate(models.Sum('amount'))['amount__sum'] or 0

    if total_amount > fixed_amount:
        messages.warning(instance.user, _('Warning: Total expenses for category "{}" exceeded {}.'.format(instance.category, fixed_amount)))
'''
# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.utils.translation import gettext as _
from .middleware import get_current_request
from .models import Expense
from django.db import models

@receiver(post_save, sender=Expense)
def check_category_expenses(sender, instance, **kwargs):
    request = get_current_request()
    if request:
        fixed_amount = 500  # Adjust this value as needed
        total_amount = Expense.objects.filter(user=instance.user, category=instance.category).aggregate(models.Sum('amount'))['amount__sum'] or 0

        if total_amount > fixed_amount:
            messages.warning(request, _('Warning: Total expenses for category "{}" exceeded {}.'.format(instance.category, fixed_amount)))
