from django.contrib import admin
from .models import Expense, UserSplit


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSplit)
class User_split_admin(admin.ModelAdmin):
    pass
