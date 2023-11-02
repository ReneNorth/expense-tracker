from django.shortcuts import render
from .models import Expense
import logging

log = logging.getLogger(__name__)


def expenses_list_view(request):
    expenses_list = Expense.objects.all()
    log.info(expenses_list)
    log.info('test logger')

    # later add pagination
    return render(request, 'expenses/expense-table.html',
                  {'expenses_list': expenses_list})
