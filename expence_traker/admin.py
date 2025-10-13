#Python modules
from typing import Optional, Sequence

#Django modules
from django.contrib.admin import register
from django.core.handlers.wsgi import WSGIRequest


#Project modules
from expence_traker.models import Category, Expense, Budget
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

@register(Category)
class CategoryAdmin(ModelAdmin):
    """ 
    Admin interface for the Category model.
    """

    list_display: Sequence[str] = ('name', 'users', 'created_at', 'updated_at', 'deleted_at')
    search_fields: Sequence[str] = ('name', 'users__username')
    list_filter: Sequence[str] = ('created_at', 'updated_at', 'deleted_at')
    ordering: Sequence[str] = ('name',)

    readonly_fields: Sequence[str] = ('created_at', 'updated_at', 'deleted_at')
    autocomplete_fields: Sequence[str] = ('users',)


@register(Expense)
class ExpenseAdmin(ModelAdmin):
    """ 
    Admin interface for the Expense model.
    """
    
    list_display: Sequence[str] = ('descrption', 'users', 'categories', 'amount', 'date', 'created_at', 'updated_at', 'deleted_at')
    search_fields: Sequence[str] = ('descrption', 'users__username', 'categories__name')
    list_filter: Sequence[str] = ('date', 'categories', 'created_at', 'updated_at', 'deleted_at')
    ordering: Sequence[str] = ('-date',)

    readonly_fields: Sequence[str] = ('created_at', 'updated_at', 'deleted_at')
    autocomplete_fields: Sequence[str] = ('users', 'categories')
    
@register(Budget)
class BudgetAdmin(ModelAdmin):
    """ 
    Admin interface for the Budget model.
    """
    
    list_display: Sequence[str] = ('users', 'monthly_limit', 'month', 'created_at', 'updated_at', 'deleted_at')
    search_fields: Sequence[str] = ('users__username',)
    list_filter: Sequence[str] = ('created_at', 'updated_at', 'deleted_at')
    ordering: Sequence[str] = ('-month',)

    readonly_fields: Sequence[str] = ('created_at', 'updated_at', 'deleted_at')
    autocomplete_fields: Sequence[str] = ('users',)
