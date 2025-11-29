# Python modules
from typing import Any, Optional

# Django REST Framework
from rest_framework.serializers import Serializer, CharField, EmailField, IntegerField, ListField
from rest_framework.exceptions import ValidationError

# Project modules
from apps.auths.models import CustomUser


class UserLoginResponseSerializer(Serializer):
    """
    Serializer for user login response.
    """

    id = IntegerField()
    full_name = CharField()
    email = EmailField()
    access = CharField()
    refresh = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "id",
            "full_name",
            "email",
            "access",
            "refresh",
        )


class UserLoginErrorsSerializer(Serializer):
    """
    Serializer for user login errors.
    """

    email = ListField(
        child=CharField(),
        required=False,
    )
    password = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "email",
            "password",
        )


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

class UserLoginSerializer(Serializer):
    """
    Serializer for user login.
    """

    email = EmailField(
        required=True,
        max_length=CustomUser.MAX_EMAIL_LENGTH,
    )
    password = CharField(
        required=True,
        max_length=CustomUser.MAX_PASSWORD_LENGTH,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "email",
            "password",
        )

    def validate_email(self, value: str) -> str:
        """Validates the email field."""
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validates the input data."""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[CustomUser] = CustomUser.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                detail={
                    "email": [f"User with email '{email}' does not exist."]
                }
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(
                detail={
                    "password": ["Incorrect password."]
                }
            )

        attrs["user"] = user    

        return super().validate(attrs)
    
class UserRegisterSerializer(Serializer):
    """
    Serializer for user registration.
    """
    password = CharField(write_only=True, required=True, min_length=8)
    email = EmailField(required=True)
    username = CharField(required=True)

    class Meta:
        """Customization of the Serializer metadata."""
        model = CustomUser
        fields = ('email', 'username','password')

    def create(self, validated_data: dict[str, Any]) -> CustomUser:
        """Create and return a new user."""
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
