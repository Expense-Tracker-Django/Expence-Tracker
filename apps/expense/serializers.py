from rest_framework.serializers import ModelSerializer, IntegerField, ValidationError
from apps.expense.models import Expense
from apps.category.models import Category

class ExpenseBaseSerializer(ModelSerializer):
    """
    Using ModelSerializer to automatically bind to a model.
    """
    category_id = IntegerField(write_only=True) 

    class Meta:
        model = Expense
        fields = ('id', 'amount', 'description', 'date', 'category_id')

class ExpenseListSerializer(ExpenseBaseSerializer):
    """
    ExpenseListSerializer
    """
    pass

class ExpenseCreateSerializer(ExpenseBaseSerializer):
    category_id = IntegerField(write_only=True, required=False, allow_null=True)

    def validate_category_id(self, value: int | None) -> int | None:
        """Validate that the category exists."""
        
        if value is None:
            return None

        request = self.context.get('request')
        if not Category.objects.filter(id=value, user=request.user).exists():
            raise ValidationError("Category does not exist.")
        return value

    def create(self, validated_data: dict) -> Expense:
        user = self.context['request'].user
        
        return Expense.objects.create(
            user=user, 
            **validated_data
        )

class ExpenseUpdateSerializer(ExpenseBaseSerializer):
    """Serializer for updating Expense instances"""
    def validate_category_id(self, value: int) -> int:
        request = self.context.get('request')
        if not Category.objects.filter(id=value, user=request.user).exists():
            raise ValidationError("Category does not exist.")
        return value