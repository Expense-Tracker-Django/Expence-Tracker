# Python modules
from typing import Any
from drf_spectacular.utils import extend_schema, OpenApiResponse

#Django modules
from django.db.models.query import QuerySet

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST, 
    HTTP_405_METHOD_NOT_ALLOWED, 
    HTTP_201_CREATED
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Project modules
from apps.abstracts.permissions import IsOwner
from apps.category.models import Category
from apps.category.serializers import (
    CategoryListSerializer, 
    CategoryCreateSerializer, 
    CategoryUpdateSerializer, 
    CategoryBaseSerializer, 
    HTTP405MethodNotAllowedSerializer
)


class CategoryViewSet(ViewSet):
    """
    A ViewSet for managing Category instances.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            HTTP_200_OK: CategoryListSerializer(many=True),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP405MethodNotAllowedSerializer,
                description="Method Not Allowed"
            ),
        },
        summary="List all categories",
        description="Retrieve a list of all category instances."
    )
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="list",
    )
    def list_categories(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """List all Category instances."""

        all_categories: QuerySet[Category] = Category.objects.all()

        serializers: CategoryListSerializer = CategoryListSerializer(
            all_categories,
            many=True,
        )

        return DRFResponse(
            data=serializers.data,
            status=HTTP_200_OK,
        )
    
    @extend_schema(
        request=CategoryCreateSerializer,
        responses={
            HTTP_201_CREATED: CategoryBaseSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=CategoryCreateSerializer,
                description="Bad Request"
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP405MethodNotAllowedSerializer,
                description="Method Not Allowed"
            ),
        },
        summary="Create a new category",
        description="Create a new category instance."
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated, IsOwner],
        url_path="create",
    )
    def create_category(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """Create a new Category instance."""

        serializer: CategoryCreateSerializer = CategoryCreateSerializer(
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

        category: Category = serializer.save()

        response_serializer: CategoryBaseSerializer = CategoryBaseSerializer(category)

        return DRFResponse(
            data=response_serializer.data,
            status=HTTP_201_CREATED,
        )
    
    @extend_schema(
        request=CategoryUpdateSerializer,
        responses={
            HTTP_200_OK: CategoryBaseSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=CategoryUpdateSerializer,
                description="Bad Request"
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP405MethodNotAllowedSerializer,
                description="Method Not Allowed"
            ),
        },
        summary="Update an existing category",
        description="Update an existing category instance."
    )
    @action(
        methods=["PUT"],
        detail=True,
        permission_classes=[IsAuthenticated, IsOwner],
        url_path="update",
    )
    def update_category(self, request: DRFRequest, pk: int, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """Update an existing Category instance."""

        try:
            category: Category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return DRFResponse(
                data={"detail": "Category not found."},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer: CategoryUpdateSerializer = CategoryUpdateSerializer(
            category,
            data=request.data,
            context={"request": request},
            partial=False,
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

        updated_category: Category = serializer.save()

        response_serializer: CategoryBaseSerializer = CategoryBaseSerializer(updated_category)

        return DRFResponse(
            data=response_serializer.data,
            status=HTTP_200_OK,
        )
    
    @extend_schema(
        responses={
            HTTP_200_OK: CategoryBaseSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=CategoryBaseSerializer,
                description="Bad Request"
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP405MethodNotAllowedSerializer,
                description="Method Not Allowed"
            ),
        },
        summary="Retrieve a category",
        description="Retrieve a specific category instance by its ID."
    )
    @action(
        methods=["GET"],
        detail=True,
        permission_classes=[IsAuthenticated, IsOwner],
        url_path="retrieve",
    )
    def retrieve_category(self, request: DRFRequest, pk: int, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """Retrieve a specific Category instance by its ID."""

        try:
            category: Category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return DRFResponse(
                data={"detail": "Category not found."},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer: CategoryBaseSerializer = CategoryBaseSerializer(category)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    
    @extend_schema(
        responses={
            HTTP_200_OK: CategoryBaseSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=CategoryBaseSerializer,
                description="Bad Request"
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP405MethodNotAllowedSerializer,
                description="Method Not Allowed"
            ),
        },
        summary="Delete a category",
        description="Delete a specific category instance by its ID."
    )
    @action(
        methods=["DELETE"],
        detail=True,
        permission_classes=[IsAuthenticated, IsOwner],
        url_path="delete",
    )
    def delete_category(self, request: DRFRequest, pk: int, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """Delete a specific Category instance by its ID."""

        try:
            category: Category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return DRFResponse(
                data={"detail": "Category not found."},
                status=HTTP_400_BAD_REQUEST,
            )

        category.delete()

        return DRFResponse(
            data={"detail": "Category deleted successfully."},
            status=HTTP_200_OK,
        )