from rest_framework import viewsets
from rest_framework.exceptions import NotFound


class BaseViewSet(viewsets.ModelViewSet):
    def get_object(self):
        try:
            return self.model.objects.get(pk=self.kwargs["pk"])
        except self.model.DoesNotExist:
            raise NotFound(self.error_message) from None

    # Добавь эти методы если их нет:
    def get_queryset(self):
        """По умолчанию возвращаем все объекты, можно переопределить в дочерних классах."""
        return self.model.objects.all()

    def perform_create(self, serializer):
        """Сохраняет объект. Можно переопределить в дочерних классах."""
        serializer.save()
