from rest_framework import serializers

from expenses.models import Expense


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'category',
                  'currency', 'who_paid', 'date', 'is_considered_debt']
