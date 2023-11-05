import logging

from django.shortcuts import render

from .models import Expense, User_split

log = logging.getLogger(__name__)


def expenses_list_view(request):
    expenses_list = Expense.objects.all().prefetch_related('split')
    for expense in expenses_list:
        expense.d = (
            expense.amount
            * expense.split.get(user__username='D').split_proportion / 100)
        expense.y = (
            expense.amount
            * expense.split.get(user__username='Y').split_proportion / 100)
    return render(request, 'expenses/expense-table.html',
                  {'expenses_list': expenses_list})
