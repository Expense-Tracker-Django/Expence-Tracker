from typing import Sequence

from django.contrib.admin import register
from .models import Expense
from unfold.admin import ModelAdmin


@register(Expense)
class ExpenseAdmin(ModelAdmin):
    """
    Admin interface for the Expense model.
    """

    list_display: Sequence[str] = (
        "descrption",
        "users",
        "categories",
        "amount",
        "date",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    search_fields: Sequence[str] = ("descrption", "users__username", "categories__name")
    list_filter: Sequence[str] = (
        "date",
        "categories",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    ordering: Sequence[str] = ("-date",)

    readonly_fields: Sequence[str] = ("created_at", "updated_at", "deleted_at")
    autocomplete_fields: Sequence[str] = ("users", "categories")
