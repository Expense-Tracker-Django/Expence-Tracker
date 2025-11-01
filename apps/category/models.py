from django.contrib.auth.models import User
from django.db.models import CASCADE, CharField, ForeignKey

from apps.abstracts.models import AbstractBaseModel


class Category(AbstractBaseModel):
    """
    Model representing an expense category.
    """

    NAME_MAX_LENGTH = 100

    name = CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="categories",
    )

    def __str__(self) -> str:
        return self.name  # type: ignore
