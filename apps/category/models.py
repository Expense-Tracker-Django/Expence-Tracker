# Django modules
from django.db.models import CASCADE, CharField, ForeignKey

from apps.abstracts.models import AbstractBaseModel
from apps.auths.models import CustomUser


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
        to=CustomUser,
        on_delete=CASCADE,
        related_name="categories",
    )

    def __str__(self) -> str:
        return self.name  # type: ignore
