from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'


def get_or_create_default_category() -> Category:
    """
    Method creates a N/A category to populate categories field in expenses
    is case of the category deletion.

    Returns:
        Category: an instance of a Category.
    """
    return Category.objects.get_or_create(name='N/A')[0]


class Expense(models.Model):
    CURRENCY_CHOICES = [
        ('kzt', 'Tenge'),
        ('eur', 'Euro'),
        ('usd', 'Dollar'),
        ('rub', 'Ruble'),
        ('sum', 'Sums'),
    ]

    description = models.TextField(max_length=100)
    amount = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET(
                                     get_or_create_default_category),
                                 blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3,
                                default='kzt')
    date = models.DateTimeField(default=timezone.now, blank=True)
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


class UserSplit(models.Model):
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
