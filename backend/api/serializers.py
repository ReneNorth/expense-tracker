from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from expenses.models import Expense, Category


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'category',
                  'currency', 'who_paid', 'date', 'is_considered_debt']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
