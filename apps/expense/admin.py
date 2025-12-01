# Python modules
from typing import Sequence
# Django modules
from django.contrib.admin import register
from django.utils.html import format_html
# Project modules
from unfold.admin import ModelAdmin
from .models import Expense


@register(Expense)
class ExpenseAdmin(ModelAdmin):
    """
    Modern and clean admin panel for Expense using Unfold.
    """

    list_display: Sequence[str] = (
        "description",
        "colored_amount",
        "user",
        "category",
        "date",
        "created_at",
    )
    list_display_links = ("description",)

    search_fields: Sequence[str] = (
        "description",
        "user__username",
        "category__name",
    )

    list_filter: Sequence[str] = (
        "category",
        "user",
        "date",
        "created_at",
    )

    ordering: Sequence[str] = ("-date",)

    autocomplete_fields: Sequence[str] = ("user", "category")

    readonly_fields: Sequence[str] = ("created_at", "updated_at", "deleted_at")

    list_per_page = 25

    def colored_amount(self, obj):
        color = "red" if obj.amount > 50000 else "green"
        return format_html(
            f'<b style="color:{color}">{obj.amount} ₸</b>'
        )

    colored_amount.short_description = "Amount"

