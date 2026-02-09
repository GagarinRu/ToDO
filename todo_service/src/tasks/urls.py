from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tasks.views import CategoryViewSet, TaskViewSet


router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
]
