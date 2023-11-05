from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from expenses.models import Expense

from .serializers import ExpensesSerializer


class ExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = ExpensesSerializer
    permission_classes = [AllowAny, ]
    queryset = Expense.objects.all()
    pagination_class = LimitOffsetPagination
