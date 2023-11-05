# Generated by Django 4.2.5 on 2023-09-10 18:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0003_alter_expense_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
