# Django REST Framework modules
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from rest_framework.exceptions import ValidationError

# Project modules
from apps.category.models import Category

class CategoryBaseSerializer(ModelSerializer):
    """Base Serializer for Category model"""

    class Meta:
        """Customization of the Serializer metadata."""

        model = Category
        fields = "__all__"


class CategoryListSerializer(CategoryBaseSerializer):
    """Serializer for listing Category instances"""
    pass


class CategoryCreateSerializer(CategoryBaseSerializer):
    """Serializer for creating Category instances"""
    name = CharField(max_length=Category.NAME_MAX_LENGTH)

    def validate_name(self, value:str) -> str:
        """Validate that the category name is unique."""

        if Category.objects.filter(name=value).exists():
            raise ValidationError("Category with this name already exists.")
        
        return value
    
    def create(self, validated_data:dict) -> Category:
        """Create a new Category instance."""
        user = self.context['request'].user
        return Category.objects.create(
            created_by=user, **validated_data
        )
    

class CategoryUpdateSerializer(CategoryBaseSerializer):
    """Serializer for updating Category instances"""
    name = CharField(max_length=Category.NAME_MAX_LENGTH, required=False)

    def validate_name(self, value:str) -> str:
        """Validate that the category name is unique."""

        category_id = self.instance.id if self.instance else None

        if Category.objects.filter(name=value).exclude(id=category_id).exists():
            raise ValidationError("Category with this name already exists.")
        
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
