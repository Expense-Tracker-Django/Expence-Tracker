from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    PROTECT,
    DateField,
    DecimalField,
    ForeignKey,
    TextField,
)

from apps.abstracts.models import AbstractBaseModel
from apps.category.models import Category


class Expense(AbstractBaseModel):
    """
    Model representing an expense entry.
    """

    description = TextField(
        blank=True,
        null="",
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="expenses",
    )
    category = ForeignKey(
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
