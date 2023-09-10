from django.db import models
from django.utils import timezone


class Expense(models.Model):
    CURRENCY_CHOICES = [
        ('kzt', 'Tenge'),
        ('eur', 'Euro'),
        ('usd', 'Dollar'),
        ('rub', 'Ruble'),
    ]

    description = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=100, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3,
                                default='kzt')
    date = models.DateField(default=timezone.now, blank=True)
    # add later relation to a 'project'

    def __str__(self) -> str:
        return self.description
