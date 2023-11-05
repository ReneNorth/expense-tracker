from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Expense(models.Model):
    CURRENCY_CHOICES = [
        ('kzt', 'Tenge'),
        ('eur', 'Euro'),
        ('usd', 'Dollar'),
        ('rub', 'Ruble'),
        ('sum', 'Sums'),
    ]

    description = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=100, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3,
                                default='kzt')
    date = models.DateField(default=timezone.now, blank=True)
    who_paid = models.ForeignKey(
        User,
        related_name='expenses',
        on_delete=models.CASCADE,
        help_text='The one who spends the money'
    )
    # split_type =
    # определять динаамически количество пользователей через лукам никнеймов или ещё как (Сколько боту на вход пришло никнеймов, столько он ожидает цифр и таким образом и раскладывает значения
    # может быть какая-то проверка по совпадению ников в чате?)
    is_considered_debt = models.BooleanField(default=True)
    # is_considered_debt = models.BooleanField(default=True)
    # add later relation to a 'project'

    def __str__(self) -> str:
        return self.description


class User_split(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='balance')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE,
                                related_name='split')
    split_proportion = models.IntegerField()  # from 0 to 10

    class Meta:
        pass
        # add check that sum of splits is equal to the total amount
        # constraints = [
        #     models.UniqueConstraint(fields=['tag', 'recipe'],
        #                             name='unique tag-recipe pair')
        # ]

    # def __str__(self):
    #     return f'{self.tag} for the recipe {self.recipe}'
