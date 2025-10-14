#Django modules
from django.db.models import (
    CharField,
    TextField,
    DateField,
    ForeignKey,
    DecimalField,
    CASCADE,
    PROTECT,
)
from django.contrib.auth.models import User

#Project modules
from abstracts.models import AbstractBaseModel

class Category(AbstractBaseModel):
    """
    Model representing an expense category.
    """

    NAME_MAX_LENGTH = 100

    name = CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )
    users = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name='categories',
    )

    def __str__(self) -> str:
        return self.name

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
        related_name='expenses',
    )
    categories = ForeignKey(
        to=Category,
        on_delete=PROTECT,
        related_name='expenses',
    )
    amount = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    date = DateField()

    def __str__(self) -> str:
        return f"{self.users} - {self.amount} on {self.date}"
    
class Budget(AbstractBaseModel):
    """
    Model representing a budget for a specific category and user.
    """

    users = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name='budgets',
    )
    monthly_limit = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    month = DateField()

    def __str__(self) -> str:
        return f"{self.users} - {self.monthly_limit} for {self.month.strftime('%B %Y')}"
    