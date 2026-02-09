from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from base.views import BaseViewSet
from base.pagination import CustomLOPagination
from tasks.constants import CATEGORY_SETTINGS, TASK_SETTINGS
from tasks.models import Category, Task
from tasks.serializers import CategorySerializer, TaskSerializer


@extend_schema(tags=[CATEGORY_SETTINGS["name"]])
class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    pagination_class = CustomLOPagination
    serializer_class = CategorySerializer
    model = Category

    def get_queryset(self):
        """Возвращает только категории текущего пользователя."""
        if self.request.user.is_authenticated:
            return Category.objects.filter(user=self.request.user)
        return Category.objects.none()

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя."""
        serializer.save(user=self.request.user)


@extend_schema(tags=[TASK_SETTINGS["name"]])
class TaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    pagination_class = CustomLOPagination
    serializer_class = TaskSerializer
    model = Task

    def get_queryset(self):
        """Возвращает только задачи текущего пользователя."""
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
        return Task.objects.none()

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Отмечает задачу как выполненную."""
        task = self.get_object()
        task.status = Task.Status.COMPLETED
        task.save()
        return Response({"status": "task completed"})
