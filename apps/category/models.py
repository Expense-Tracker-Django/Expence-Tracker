from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, CharField, ForeignKey

from abstracts.models import AbstractBaseModel


# Create your models here.
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
        related_name="categories",
    )

    def __str__(self) -> str:
        return self.name  # type: ignore
