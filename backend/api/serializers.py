from rest_framework import serializers
from expenses.models import Expense


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'category',
                  'currency', 'date']
