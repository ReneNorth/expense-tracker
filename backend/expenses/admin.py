from django.contrib import admin
from .models import Expense, UserSplit, Category


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'amount', 'currency',
                    'date', 'who_paid']
    list_filter = ['date', 'who_paid']


@admin.register(UserSplit)
class UserSplitAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
