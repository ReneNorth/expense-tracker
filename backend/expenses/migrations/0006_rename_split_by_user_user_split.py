# Generated by Django 4.2.5 on 2023-11-05 09:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("expenses", "0005_expense_is_considered_debt_expense_who_paid_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Split_by_user",
            new_name="User_split",
        ),
    ]