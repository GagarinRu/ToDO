from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from tasks.models import Category, Task


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ("id", "user", "name", "color")
        read_only_fields = ("id", "user")  # Добавляем user в read_only


class TaskSerializer(ModelSerializer):
    categories = PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "completed_at",
            "user",
            "categories",
        )
        read_only_fields = ("id", "user", "completed_at")  # user теперь read_only
