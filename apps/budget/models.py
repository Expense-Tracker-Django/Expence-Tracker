from django.contrib.auth.models import User
from django.db.models import CASCADE, DateField, DecimalField, ForeignKey

from apps.abstracts.models import AbstractBaseModel


class Budget(AbstractBaseModel):
    """
    Model representing a budget for a specific category and user.
    """

    users = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="budgets",
    )
    monthly_limit = DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    month = DateField()

    def __str__(self) -> str:
        return f"{self.users} - {self.monthly_limit} for {self.month.strftime('%B %Y')}"  # type: ignore
