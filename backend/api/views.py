from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from expenses.models import Expense, Category

from .serializers import ExpensesSerializer, CategorySerializer


class ExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = ExpensesSerializer
    permission_classes = [AllowAny, ]
    queryset = Expense.objects.all()
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
