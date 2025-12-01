# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.category.views import CategoryViewSet


router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    prefix="categories",
    viewset=CategoryViewSet,
    basename="category",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]