from typing import Sequence

from django.contrib.admin import register
from .models import Budget
from unfold.admin import ModelAdmin


@register(Budget)
class BudgetAdmin(ModelAdmin):
    """
    Admin interface for the Budget model.
    """

    list_display: Sequence[str] = (
        "user",
        "monthly_limit",
        "month",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    search_fields: Sequence[str] = ("users__username",)
    list_filter: Sequence[str] = ("created_at", "updated_at", "deleted_at")
    ordering: Sequence[str] = ("-month",)

    readonly_fields: Sequence[str] = ("created_at", "updated_at", "deleted_at")
    autocomplete_fields: Sequence[str] = ("user",)
