from django.contrib import admin
from .models import Expense, User_split


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass


@admin.register(User_split)
class User_split_admin(admin.ModelAdmin):
    pass
