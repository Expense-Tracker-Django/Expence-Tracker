# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.expense.views import ExpenseViewSet


router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    prefix="expenses",
    viewset=ExpenseViewSet,
    basename="expense",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]