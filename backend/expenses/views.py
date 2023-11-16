import logging
from django.shortcuts import render, get_object_or_404
from .models import Expense

log = logging.getLogger(__name__)


def expenses_list_view(request) -> render:
    """_summary_
    Retruns all expenses and its splits from the database. 
    If expenses split exists, then returns it
    Otherwise adds a split 100 - 0 with a warinign 
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    expenses_list = Expense.objects.all(
    ).prefetch_related('split').order_by('-date')
    for expense in expenses_list:
        if expense.split.exists():
            split_d = expense.split.get(user__username='D').split_proportion
            split_y = expense.split.get(user__username='Y').split_proportion
            expense.d = (expense.amount * split_d / 100)
            expense.y = (expense.amount * split_y / 100)
        else:
            expense.d = (expense.amount * 0 / 100)
            expense.y = (expense.amount * 100 / 100)
            expense.description += ' (Warning: the split was not specified)'
    return render(request, 'expenses/expense-table.html',
                  {'expenses_list': expenses_list})

