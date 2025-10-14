from category.models import Category
from django.contrib.auth.models import User
from django.db.models import (CASCADE, PROTECT, DateField, DecimalField,
                              ForeignKey, TextField)

from abstracts.models import AbstractBaseModel


class Expense(AbstractBaseModel):
    """
    Model representing an expense entry.
    """

    descrption = TextField(
        blank=True,
        null="",
    )
    users = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="expenses",
    )
    categories = ForeignKey(
        to=Category,
        on_delete=PROTECT,
        related_name="expenses",
    )
    amount = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    date = DateField()

    def __str__(self) -> str:
        return f"{self.users} - {self.amount} on {self.date}"
