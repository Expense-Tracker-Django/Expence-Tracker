# Python modules
from typing import Any
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

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
    HTTP_201_CREATED,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Project modules
from apps.abstracts.permissions import IsOwner
from apps.expense.models import Expense
from apps.expense.serializers import (
    ExpenseListSerializer, 
    ExpenseCreateSerializer, 
    ExpenseUpdateSerializer,
    ExpenseBaseSerializer,
)

class ExpenseViewSet(ViewSet):
    """ViewSet for managing Expense instances."""
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            HTTP_200_OK: ExpenseListSerializer(many=True),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP_405_METHOD_NOT_ALLOWED,
                description="Method not allowed."
            ),
        },
        summary = "List expenses with filters",
        description="Filters: date_from, date_to, category, min_amount, max_amount",
        parameters=[
            OpenApiParameter(
                name='date_from',
                required=False,
            ),
            OpenApiParameter(
                name='date_to',
                required=False,
            ),
            OpenApiParameter(
                name='category_id',
                required=False,
            ),
            OpenApiParameter(
                name='min_amount',
                required=False,
            ),
            OpenApiParameter(
                name='max_amount',
                required=False,
            )
        ]
    )
    @action(
        detail=False, 
        methods=["GET"],
        permission_classes=[IsAuthenticated, IsOwner],
        url_path='list',
    )
    def list_expenses(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """List all expenses for the authenticated user."""

        all_expenses: QuerySet = Expense.objects.filter(user=request.user).order_by("-date")


        date_from: str = request.query_params.get("date_from", None)
        date_to: str = request.query_params.get("date_to", None)
        category_id: str = request.query_params.get("category_id", None)
        min_amount: str = request.query_params.get("min_amount", None)
        max_amount: str = request.query_params.get("max_amount", None)

        if date_from:
            all_expenses = all_expenses.filter(date__gte=date_from)

        if date_to:
            all_expenses = all_expenses.filter(date__lte=date_to)

        if category_id:
            all_expenses = all_expenses.filter(category_id=category_id)

        if min_amount:
            all_expenses = all_expenses.filter(amount__gte=min_amount)

        if max_amount:
            all_expenses = all_expenses.filter(amount__lte=max_amount)

        serializer: ExpenseListSerializer = ExpenseListSerializer(all_expenses, many=True)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    
    
    @extend_schema(
        request=ExpenseCreateSerializer,
        responses={
            HTTP_201_CREATED: ExpenseListSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ExpenseBaseSerializer,
                description="Bad request."
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP_405_METHOD_NOT_ALLOWED,
                description="Method not allowed."
            ),
        },
        summary="Create an expense",
    )
    @action(
        detail=False, 
        methods=["POST"],
        permission_classes=[IsAuthenticated, IsOwner],
        url_path='create',
    )
    def create_expense(
        self, 
        request: DRFRequest, 
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any],
        ) -> DRFResponse:
        """Create a new expense for the authenticated user."""

        serializer: ExpenseCreateSerializer = ExpenseCreateSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            expense: Expense = serializer.save()
            response_serializer: ExpenseListSerializer = ExpenseListSerializer(expense)
            return DRFResponse(
                data=response_serializer.data,
                status=HTTP_201_CREATED,
            )
        
        return DRFResponse(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST,
        )
    

    @extend_schema(
        request=ExpenseUpdateSerializer,
        responses={
            HTTP_200_OK: ExpenseListSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ExpenseBaseSerializer,
                description="Bad request."
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP_405_METHOD_NOT_ALLOWED,
                description="Method not allowed."
            ),
        },
        summary="Update expenses"
    )
    @action(
        detail=True, 
        methods=["PUT"],
        permission_classes=[IsAuthenticated, IsOwner],
        url_path='update',
    )
    def update_expense(
        self, 
        request: DRFRequest, 
        pk: int,
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any],
        ) -> DRFResponse:
        """Update an existing expense for the authenticated user."""

        try:
            expense: Expense = Expense.objects.get(id=pk, user=request.user)
        except Expense.DoesNotExist:
            return DRFResponse(
                data={"detail": "Expense not found."},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer: ExpenseUpdateSerializer = ExpenseUpdateSerializer(
            expense,
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            updated_expense: Expense = serializer.save()
            response_serializer: ExpenseListSerializer = ExpenseListSerializer(updated_expense)
            return DRFResponse(
                data=response_serializer.data,
                status=HTTP_200_OK,
            )
        
        return DRFResponse(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST,
        )
    
    @extend_schema(
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Expense deleted successfully."
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ExpenseBaseSerializer,
                description="Bad request."
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                response=HTTP_405_METHOD_NOT_ALLOWED,
                description="Method not allowed."
            ),
        },
        summary="Delete expense"
    )
    @action(
        detail=True, 
        methods=["DELETE"],
        permission_classes=[IsAuthenticated, IsOwner],
        url_path='delete',
    )
    def delete_expense(
        self, 
        request: DRFRequest, 
        pk: int,
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any],
        ) -> DRFResponse:
        """Delete an existing expense for the authenticated user."""

        try:
            expense: Expense = Expense.objects.get(id=pk, user=request.user)
        except Expense.DoesNotExist:
            return DRFResponse(
                data={"detail": "Expense not found."},
                status=HTTP_400_BAD_REQUEST,
            )

        expense.delete()
        return DRFResponse(
            data={"detail": "Expense deleted successfully."},
            status=HTTP_200_OK,
        )
    
        



        


