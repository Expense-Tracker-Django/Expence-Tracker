#Django REST Framework modules
from rest_framework.serializers import Serializer, CharField, IntegerField, DecimalField, DateField
from rest_framework.exceptions import ValidationError

# Project modules
from apps.expense.models import Expense
from apps.category.models import Category

class ExpenseBaseSerializer(Serializer):
    """Base Serializer for Expense model"""
    AMOUNT_MAX_DIGITS = 10
    AMOUNT_DECIMAL_PLACES = 2
    id = IntegerField(read_only=True)
    amount = DecimalField(max_digits=AMOUNT_MAX_DIGITS, decimal_places=AMOUNT_DECIMAL_PLACES)
    description = CharField()
    date = DateField()
    category_id = IntegerField()

    class Meta:
        """Customization of the Serializer metadata."""
        model = Expense
        fields = "__all__"


class ExpenseListSerializer(ExpenseBaseSerializer):
    """Serializer for listing Expense instances"""
    pass


class ExpenseCreateSerializer(ExpenseBaseSerializer):
    """Serializer for creating Expense instances"""

    def validate_category_id(self, value:int) -> int:
        """Validate that the category exists."""

        request = self.context['request']
        if not Category.objects.filter(id=value, created_by=request.user).exists():
            raise ValidationError("Category does not exist.")
        return value
    
    def create(self, validated_data:dict) -> Expense:
        """Create a new Expense instance."""
        user = self.context['request'].user
        return Expense.objects.create(
            user=user, 
            **validated_data,
        )
    

class ExpenseUpdateSerializer(ExpenseBaseSerializer):
    """Serializer for updating Expense instances"""

    def validate_category_id(self, value:int) -> int:
        """Validate that the category exists."""

        request = self.context['request']
        if not Category.objects.filter(id=value, created_by=request.user).exists():
            raise ValidationError("Category does not exist.")
        return value
    
class HTTP405MethodNotAllowedSerializer(Serializer):
    """
    Serializer for HTTP 405 Method Not Allowed response.
    """

    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "detail",
        )
