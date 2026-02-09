from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from users.models import User
from users.serializers import UserSerializer, TelegramAuthSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        request=TelegramAuthSerializer,
        responses={200: {"access": "string", "refresh": "string"}},
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def telegram_auth(self, request):
        """Аутентификация через Telegram."""
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = serializer.get_tokens(user)
        return Response(tokens)

    @extend_schema(responses={200: UserSerializer})
    @action(detail=False, methods=["get"], url_path=r"telegram/(?P<telegram_id>\d+)")
    def get_by_telegram(self, request, telegram_id=None):
        """Получить пользователя по Telegram ID."""
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
