from typing import Sequence

from django.contrib.admin import register
from .models import Category
from unfold.admin import ModelAdmin


@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Admin interface for the Category model.
    """

    list_display: Sequence[str] = (
        "name",
        "user",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    search_fields: Sequence[str] = ("name", "users__username")
    list_filter: Sequence[str] = ("created_at", "updated_at", "deleted_at")
    ordering: Sequence[str] = ("name",)

    readonly_fields: Sequence[str] = ("created_at", "updated_at", "deleted_at")
    autocomplete_fields: Sequence[str] = ("user",)
